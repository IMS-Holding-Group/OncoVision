#!/usr/bin/env python3
"""
OncoVision - Flask Web Application
Web interface for mammogram analysis using YOLOv8
"""

import os
import json
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from ultralytics import YOLO
import torch

# Fix PyTorch 2.6 compatibility issue
try:
    torch.serialization.add_safe_globals([
        'ultralytics.nn.tasks.DetectionModel',
        'ultralytics.nn.modules.block.C2f',
        'ultralytics.nn.modules.conv.Conv',
        'ultralytics.nn.modules.head.Detect',
        'ultralytics.nn.modules.block.SPPF',
        'ultralytics.nn.modules.block.Bottleneck'
    ])
except AttributeError:
    # For older PyTorch versions
    pass

# Import our inference module
from infer import OncoVisionInference

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate random secret key

# Configuration
UPLOAD_FOLDER = Path('uploads')
RESULTS_FOLDER = Path('inference_results')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create directories
UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize inference engine
try:
    inference_engine = OncoVisionInference()
    MODEL_LOADED = True
except Exception as e:
    print(f"⚠️  Warning : Could not load model - {e}")
    inference_engine = None
    MODEL_LOADED = False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Get database connection with proper timeout and WAL mode"""
    conn = sqlite3.connect('oncovision.db', timeout=30.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    # Set busy timeout
    conn.execute("PRAGMA busy_timeout=30000")
    return conn

def init_database():
    """Initialize database with proper schema"""
    try:
        conn = get_db_connection()
        
        # Create analysis_results table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_name TEXT NOT NULL,
                tumor_detected BOOLEAN NOT NULL,
                num_detections INTEGER DEFAULT 0,
                max_confidence REAL DEFAULT 0.0,
                avg_confidence REAL DEFAULT 0.0,
                processing_time REAL DEFAULT 0.0,
                annotated_image_path TEXT,
                created_at TEXT NOT NULL,
                user_id INTEGER,
                model_version TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create system_logs table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                module TEXT,
                user_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create users table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT
            )
        """)
        
        # Create detections table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result_id INTEGER NOT NULL,
                confidence REAL NOT NULL,
                x_min REAL NOT NULL,
                y_min REAL NOT NULL,
                x_max REAL NOT NULL,
                y_max REAL NOT NULL,
                FOREIGN KEY (result_id) REFERENCES analysis_results (id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

def safe_db_operation(operation_func, *args, **kwargs):
    """Safely execute database operations with proper connection handling"""
    conn = None
    try:
        conn = get_db_connection()
        result = operation_func(conn, *args, **kwargs)
        conn.commit()
        return result
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def log_system_event(level, message, module=None, user_id=None):
    """Log system events to database"""
    try:
        def log_operation(conn):
            conn.execute("""
                INSERT INTO system_logs (level, message, module, user_id)
                VALUES (?, ?, ?, ?)
            """, (level, message, module, user_id))
        
        safe_db_operation(log_operation)
    except Exception as e:
        print(f"Logging error : {e}")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """Verify password against hash"""
    return hash_password(password) == hash_value

def login_required(f):
    """Decorator for routes that require login"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', model_loaded=MODEL_LOADED)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND is_active = 1',
            (username,)
        ).fetchone()
        conn.close()
        
        if user and verify_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # Update last login
            conn = get_db_connection()
            conn.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now().isoformat(), user['id'])
            )
            conn.commit()
            conn.close()
            
            log_system_event('INFO', f'User {username} logged in', 'auth', user['id'])
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            log_system_event('WARNING', f'Failed login attempt for {username}', 'auth')
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    username = session.get('username', 'Unknown')
    log_system_event('INFO', f'User {username} logged out', 'auth', session.get('user_id'))
    session.clear()
    flash('Logout successful', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    conn = get_db_connection()
    
    # Get recent analyses from analysis_results table
    try:
        recent_analyses_raw = conn.execute("""
            SELECT * FROM analysis_results 
            ORDER BY created_at DESC 
            LIMIT 10
        """).fetchall()
        
        # Convert to list of dicts
        recent_analyses = []
        for analysis in recent_analyses_raw:
            analysis_dict = dict(analysis)
            # Convert timestamp to readable format
            if 'created_at' in analysis_dict and analysis_dict['created_at']:
                if isinstance(analysis_dict['created_at'], str):
                    analysis_dict['timestamp'] = analysis_dict['created_at'][:19].replace('T', ' ')
                else:
                    analysis_dict['timestamp'] = str(analysis_dict['created_at'])[:19].replace(' ', ' ')
            recent_analyses.append(analysis_dict)
            
    except sqlite3.OperationalError:
        # Fallback if table doesn't exist
        recent_analyses = []
    
    # Get summary statistics
    try:
        stats = conn.execute("""
            SELECT 
                COUNT(*) as total_analyses,
                SUM(CASE WHEN tumor_detected = 1 THEN 1 ELSE 0 END) as tumor_detected_count,
                SUM(num_detections) as total_detections,
                AVG(max_confidence) as avg_confidence
            FROM analysis_results
        """).fetchone()
    except sqlite3.OperationalError:
        # Fallback if table doesn't exist
        stats = {
            'total_analyses': 0,
            'tumor_detected_count': 0,
            'total_detections': 0,
            'avg_confidence': 0.0
        }
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_analyses=recent_analyses,
                         stats=stats)

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    """Analysis page"""
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'success' : False, 'error' : 'No file selected'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success' : False, 'error' : 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success' : False, 'error' : 'File type not supported. Please use: PNG, JPG, JPEG, BMP, TIFF'}), 400
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            filepath = app.config['UPLOAD_FOLDER'] / unique_filename
            file.save(filepath)
            
            # Get analysis parameters
            conf_threshold = float(request.form.get('confidence', 0.5))
            iou_threshold = float(request.form.get('iou', 0.45))
            
            start_time = datetime.now()
            
            if MODEL_LOADED and inference_engine:
                # Use trained model for real tumor detection
                result, annotated_image = inference_engine.run_inference(
                    image_path=filepath,
                    conf_threshold=conf_threshold,
                    iou_threshold=iou_threshold,
                    save_results=True
                )
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Save annotated image for web display
                annotated_filename = f"web_annotated_{unique_filename}"
                annotated_path = RESULTS_FOLDER / annotated_filename
                annotated_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(str(annotated_path), annotated_bgr)
                
                # Save analysis results to database
                def save_analysis_result(conn):
                    conn.execute("""
                        INSERT INTO analysis_results 
                        (image_name, tumor_detected, num_detections, max_confidence, avg_confidence, 
                         processing_time, annotated_image_path, created_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        unique_filename,
                        result['summary']['tumor_detected'],
                        result['summary']['num_detections'],
                        result['summary']['max_confidence'],
                        result['summary']['avg_confidence'],
                        processing_time,
                        annotated_filename,
                        datetime.now().isoformat(),
                        session.get('user_id')
                    ))
                
                safe_db_operation(save_analysis_result)
                
                # Log analysis
                log_system_event('INFO', 
                                f'Analysis completed for {unique_filename} - Tumor: {result["summary"]["tumor_detected"]}',
                                'analysis', session['user_id'])
                
                return jsonify({
                    'success' : True,
                    'tumor_detected' : result['summary']['tumor_detected'],
                    'detections' : result['predictions'],
                    'max_confidence' : result['summary']['max_confidence'],
                    'avg_confidence' : result['summary']['avg_confidence'],
                    'num_detections' : result['summary']['num_detections'],
                    'processing_time' : processing_time,
                    'annotated_image_url' : f'/result_image/{annotated_filename}'
                })
            else:
                # Return error if model not loaded
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Save failed analysis to database
                def save_failed_analysis(conn):
                    conn.execute("""
                        INSERT INTO analysis_results 
                        (image_name, tumor_detected, num_detections, max_confidence, avg_confidence, 
                         processing_time, created_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        unique_filename,
                        False,
                        0,
                        0.0,
                        0.0,
                        processing_time,
                        datetime.now().isoformat(),
                        session.get('user_id')
                    ))
                
                safe_db_operation(save_failed_analysis)
                
                log_system_event('ERROR', f'Analysis failed - Model not loaded for {unique_filename}', 'analysis', session.get('user_id'))
                
                return jsonify({
                    'success' : False,
                    'error' : 'Model not loaded. Please check system settings and ensure the trained model is available.',
                    'processing_time' : processing_time
                })
                
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Save failed analysis to database
            try:
                def save_error_analysis(conn):
                    conn.execute("""
                        INSERT INTO analysis_results 
                        (image_name, tumor_detected, num_detections, max_confidence, avg_confidence, 
                         processing_time, created_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        unique_filename,
                        False,
                        0,
                        0.0,
                        0.0,
                        processing_time,
                        datetime.now().isoformat(),
                        session.get('user_id')
                    ))
                
                safe_db_operation(save_error_analysis)
            except:
                pass  # Don't fail if database save fails
            
            log_system_event('ERROR', f'Analysis failed : {str(e)}', 'analysis', session.get('user_id'))
            return jsonify({'success' : False, 'error' : f'Analysis error occurred: {str(e)}'}), 500
    
    return render_template('analyze.html', model_loaded=MODEL_LOADED)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file upload and analysis"""
    if not MODEL_LOADED:
        return jsonify({'error' : 'Model not loaded. Please check system settings.'}), 500
    
    if 'file' not in request.files:
        return jsonify({'error' : 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error' : 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error' : 'File type not supported. Please use: PNG, JPG, JPEG, BMP, TIFF'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = app.config['UPLOAD_FOLDER'] / unique_filename
        file.save(filepath)
        
        # Get analysis parameters
        conf_threshold = float(request.form.get('confidence', 0.25))
        iou_threshold = float(request.form.get('iou', 0.45))
        
        # Run inference
        start_time = datetime.now()
        result, annotated_image = inference_engine.run_inference(
            image_path=filepath,
            conf_threshold=conf_threshold,
            iou_threshold=iou_threshold,
            save_results=True
        )
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Update database with processing time
        conn = get_db_connection()
        conn.execute("""
            UPDATE analysis_results 
            SET processing_time = ?, model_version = ?
            WHERE image_name = ?
        """, (processing_time, str(inference_engine.model_path), unique_filename))
        conn.commit()
        conn.close()
        
        # Save annotated image for web display
        annotated_path = RESULTS_FOLDER / f"web_annotated_{unique_filename}"
        annotated_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(annotated_path), annotated_bgr)
        
        # Log analysis
        log_system_event('INFO', 
                        f'Analysis completed for {filename} - Tumor : {result["summary"]["tumor_detected"]}',
                        'analysis', session['user_id'])
        
        # Prepare response
        response_data = {
            'success' : True,
            'result' : result,
            'annotated_image' : f'/result_image/{annotated_path.name}',
            'processing_time' : processing_time
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        log_system_event('ERROR', f'Analysis failed for {filename} : {str(e)}', 'analysis', session['user_id'])
        return jsonify({'error' : f'Failed to analyze image: {str(e)}'}), 500

@app.route('/result_image/<filename>')
def result_image(filename):
    """Serve result images"""
    return send_file(RESULTS_FOLDER / filename)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve original uploaded images from UPLOAD_FOLDER"""
    return send_file(app.config['UPLOAD_FOLDER'] / filename)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon or return 204 if not found"""
    try:
        return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')
    except:
        # Return empty response to prevent 404
        from flask import Response
        return Response('', status=204)

@app.route('/history')
@login_required
def history():
    """Analysis history page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    
    # Get total count
    total = conn.execute('SELECT COUNT(*) FROM analysis_results').fetchone()[0]
    
    # Get paginated results
    analyses = conn.execute("""
        SELECT ar.*, COUNT(d.id) as detection_count
        FROM analysis_results ar
        LEFT JOIN detections d ON ar.id = d.result_id
        GROUP BY ar.id
        ORDER BY ar.created_at DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset)).fetchall()
    
    conn.close()
    
    # Calculate pagination info
    total_pages = (total + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template('history.html',
                         analyses=analyses,
                         page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next)

@app.route('/analysis/<int:analysis_id>')
@login_required
def analysis_detail(analysis_id):
    """View detailed analysis results"""
    conn = get_db_connection()
    
    # Check if user_id column exists first
    try:
        analysis = conn.execute("""
            SELECT * FROM analysis_results WHERE id = ? AND user_id = ?
        """, (analysis_id, session['user_id'])).fetchone()
    except sqlite3.OperationalError:
        # user_id column doesn't exist, fallback to simple query
        analysis = conn.execute("""
            SELECT * FROM analysis_results WHERE id = ?
        """, (analysis_id,)).fetchone()
    
    if not analysis:
        conn.close()
        flash('Analysis not found', 'error')
        return redirect(url_for('history'))
    
    # Convert analysis to dict for easier template access
    analysis_dict = dict(analysis)
    
    # Parse created_at if it's a string
    if isinstance(analysis_dict['created_at'], str):
        try:
            from datetime import datetime
            analysis_dict['created_at'] = datetime.fromisoformat(analysis_dict['created_at'].replace('Z', '+00:00'))
        except:
            # If parsing fails, keep as string
            pass
    
    # Get detections
    detections = conn.execute("""
        SELECT * FROM detections WHERE result_id = ?
        ORDER BY confidence DESC
    """, (analysis_id,)).fetchall()
    
    conn.close()
    
    return render_template('analysis_detail.html',
                         analysis=analysis_dict,
                         detections=detections)

@app.route('/analysis/<int:analysis_id>/delete', methods=['POST'])
@login_required
def delete_analysis(analysis_id):
    """Delete an analysis, its detections, and related files"""
    conn = get_db_connection()
    # Try to restrict by user when possible
    try:
        analysis = conn.execute(
            """
            SELECT * FROM analysis_results WHERE id = ? AND user_id = ?
            """,
            (analysis_id, session['user_id'])
        ).fetchone()
    except sqlite3.OperationalError:
        analysis = conn.execute(
            """
            SELECT * FROM analysis_results WHERE id = ?
            """,
            (analysis_id,)
        ).fetchone()

    if not analysis:
        conn.close()
        flash('Analysis not found', 'error')
        return redirect(url_for('history'))

    # Delete detections first
    conn.execute('DELETE FROM detections WHERE result_id = ?', (analysis_id,))
    # Delete analysis row
    conn.execute('DELETE FROM analysis_results WHERE id = ?', (analysis_id,))
    conn.commit()
    conn.close()

    # Remove files (best-effort)
    try:
        image_name = analysis['image_name']
        if image_name:
            original_path = app.config['UPLOAD_FOLDER'] / image_name
            if original_path.exists():
                try:
                    original_path.unlink()
                except Exception:
                    pass
            # Remove potential annotated copies
            from pathlib import Path as P
            candidates = [
                RESULTS_FOLDER / f"web_annotated_{image_name}",
                RESULTS_FOLDER / image_name,
                P('static/results') / f"web_annotated_{image_name}"
            ]
            for p in candidates:
                try:
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass
    except Exception:
        pass

    flash('Analysis deleted', 'success')
    return redirect(url_for('history'))

@app.route('/statistics')
@login_required
def statistics():
    """Statistics page"""
    conn = get_db_connection()
    
    # Get analysis results for current user
    try:
        analyses = conn.execute("""
            SELECT * FROM analysis_results 
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (session['user_id'],)).fetchall()
    except sqlite3.OperationalError:
        # user_id column doesn't exist, get all analyses
        analyses = conn.execute("""
            SELECT * FROM analysis_results 
            ORDER BY created_at DESC
        """).fetchall()
    
    # Get detection statistics from analysis_results
    try:
        detection_stats_raw = conn.execute("""
            SELECT 
                tumor_detected,
                num_detections,
                max_confidence,
                processing_time,
                created_at
            FROM analysis_results 
            WHERE user_id = ?
        """, (session['user_id'],)).fetchall()
    except sqlite3.OperationalError:
        detection_stats_raw = conn.execute("""
            SELECT 
                tumor_detected,
                num_detections,
                max_confidence,
                processing_time,
                created_at
            FROM analysis_results
        """).fetchall()
    
    # Convert detection_stats to list of dicts with datetime conversion
    detection_stats = []
    for stat in detection_stats_raw:
        stat_dict = dict(stat)
        # Convert created_at string to datetime object
        if isinstance(stat_dict['created_at'], str):
            try:
                from datetime import datetime
                stat_dict['created_at'] = datetime.fromisoformat(stat_dict['created_at'].replace('Z', '+00:00'))
            except:
                # If parsing fails, keep as string
                pass
        detection_stats.append(stat_dict)
    
    # Get recent activity from analysis_results
    try:
        recent_activity_raw = conn.execute("""
            SELECT 
                id,
                image_name,
                tumor_detected,
                created_at,
                max_confidence
            FROM analysis_results
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        """, (session['user_id'],)).fetchall()
    except sqlite3.OperationalError:
        recent_activity_raw = conn.execute("""
            SELECT 
                id,
                image_name,
                tumor_detected,
                created_at,
                max_confidence
            FROM analysis_results
            ORDER BY created_at DESC
            LIMIT 10
        """).fetchall()
    
    # Convert recent_activity to list of dicts with datetime conversion
    recent_activity = []
    for activity in recent_activity_raw:
        activity_dict = dict(activity)
        # Convert created_at string to datetime object
        if isinstance(activity_dict['created_at'], str):
            try:
                from datetime import datetime
                activity_dict['created_at'] = datetime.fromisoformat(activity_dict['created_at'].replace('Z', '+00:00'))
            except:
                # If parsing fails, keep as string
                pass
        recent_activity.append(activity_dict)
    
    # Create summary data by grouping by date
    summary = []
    if analyses:
        from collections import defaultdict
        daily_stats = defaultdict(lambda : {'total' : 0, 'positive' : 0, 'negative' : 0})
        
        for analysis in analyses:
            # Extract date from created_at
            if isinstance(analysis['created_at'], str):
                date_str = analysis['created_at'].split(' ')[0] if ' ' in analysis['created_at'] else analysis['created_at']
            else:
                date_str = analysis['created_at'].strftime('%Y-%m-%d')
            daily_stats[date_str]['total'] += 1
            if analysis['tumor_detected']:
                daily_stats[date_str]['positive'] += 1
            else:
                daily_stats[date_str]['negative'] += 1
        
        # Convert to list format for template
        for date, stats in daily_stats.items():
            summary.append({
                'analysis_date' : date,
                'total_analyses' : stats['total'],
                'positive_cases' : stats['positive'],
                'negative_cases' : stats['negative']
            })
    
    conn.close()
    
    return render_template('statistics.html',
                         summary=summary,
                         detection_stats=detection_stats,
                         recent_activity=recent_activity)

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for statistics data"""
    conn = get_db_connection()
    
    # Daily analysis counts for chart
    daily_stats = conn.execute("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as total,
            SUM(CASE WHEN tumor_detected = 1 THEN 1 ELSE 0 END) as tumor_detected
        FROM analysis_results
        WHERE DATE(created_at) >= DATE('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date
    """).fetchall()
    
    # Confidence distribution
    confidence_dist = conn.execute("""
        SELECT 
            ROUND(confidence, 1) as conf_range,
            COUNT(*) as count
        FROM detections
        GROUP BY ROUND(confidence, 1)
        ORDER BY conf_range
    """).fetchall()
    
    conn.close()
    
    return jsonify({
        'daily_stats' : [dict(row) for row in daily_stats],
        'confidence_distribution' : [dict(row) for row in confidence_dist]
    })

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_code=404,
                         error_message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    log_system_event('ERROR', f'Internal server error : {str(error)}', 'web')
    return render_template('error.html',
                         error_code=500,
                         error_message='Internal server error'), 500

@app.errorhandler(413)
def too_large(error):
    """Handle file too large errors"""
    return jsonify({'error' : 'File too large. Maximum size is 16 MB'}), 413

if __name__ == '__main__':
    print("🔬 OncoVision Web Application")
    print("=" * 50)
    
    # Initialize database
    init_database()
    
    if not MODEL_LOADED:
        print("⚠️  Warning : Model not loaded. Some features may not work.")
        print("   Please ensure model exists at : models/oncovision_latest.pt")
    
    print(f"🌐 Starting web server...")
    print(f"📁 Upload folder : {UPLOAD_FOLDER.absolute()}")
    print(f"📁 Results folder : {RESULTS_FOLDER.absolute()}")
    print(f"🔗 Access the application at : http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
