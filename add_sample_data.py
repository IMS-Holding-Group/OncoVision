#!/usr/bin/env python3
"""
Script to add sample analysis data to OncoVision database
"""

import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('oncovision.db', timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn

def add_sample_analyses():
    """Add sample analysis data"""
    print("🔬 Adding sample analysis data...")
    
    try:
        conn = get_db_connection()
        
        # Sample analysis data
        sample_analyses = [
            {
                'image_name': '20240920_120000_mammogram_001.jpg',
                'tumor_detected': True,
                'num_detections': 2,
                'max_confidence': 0.87,
                'avg_confidence': 0.72,
                'processing_time': 3.2,
                'annotated_image_path': 'web_annotated_20240920_120000_mammogram_001.jpg',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_130000_mammogram_002.jpg',
                'tumor_detected': False,
                'num_detections': 0,
                'max_confidence': 0.0,
                'avg_confidence': 0.0,
                'processing_time': 2.8,
                'annotated_image_path': 'web_annotated_20240920_130000_mammogram_002.jpg',
                'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_140000_mammogram_003.jpg',
                'tumor_detected': True,
                'num_detections': 1,
                'max_confidence': 0.94,
                'avg_confidence': 0.94,
                'processing_time': 4.1,
                'annotated_image_path': 'web_annotated_20240920_140000_mammogram_003.jpg',
                'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_150000_mammogram_004.jpg',
                'tumor_detected': True,
                'num_detections': 3,
                'max_confidence': 0.76,
                'avg_confidence': 0.68,
                'processing_time': 3.7,
                'annotated_image_path': 'web_annotated_20240920_150000_mammogram_004.jpg',
                'created_at': (datetime.now() - timedelta(days=4)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_160000_mammogram_005.jpg',
                'tumor_detected': False,
                'num_detections': 0,
                'max_confidence': 0.0,
                'avg_confidence': 0.0,
                'processing_time': 2.5,
                'annotated_image_path': 'web_annotated_20240920_160000_mammogram_005.jpg',
                'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_170000_mammogram_006.jpg',
                'tumor_detected': True,
                'num_detections': 1,
                'max_confidence': 0.89,
                'avg_confidence': 0.89,
                'processing_time': 3.9,
                'annotated_image_path': 'web_annotated_20240920_170000_mammogram_006.jpg',
                'created_at': (datetime.now() - timedelta(days=6)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_180000_mammogram_007.jpg',
                'tumor_detected': False,
                'num_detections': 0,
                'max_confidence': 0.0,
                'avg_confidence': 0.0,
                'processing_time': 2.3,
                'annotated_image_path': 'web_annotated_20240920_180000_mammogram_007.jpg',
                'created_at': (datetime.now() - timedelta(days=7)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_190000_mammogram_008.jpg',
                'tumor_detected': True,
                'num_detections': 2,
                'max_confidence': 0.82,
                'avg_confidence': 0.75,
                'processing_time': 4.2,
                'annotated_image_path': 'web_annotated_20240920_190000_mammogram_008.jpg',
                'created_at': (datetime.now() - timedelta(days=8)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_200000_mammogram_009.jpg',
                'tumor_detected': False,
                'num_detections': 0,
                'max_confidence': 0.0,
                'avg_confidence': 0.0,
                'processing_time': 2.7,
                'annotated_image_path': 'web_annotated_20240920_200000_mammogram_009.jpg',
                'created_at': (datetime.now() - timedelta(days=9)).isoformat(),
                'user_id': 1
            },
            {
                'image_name': '20240920_210000_mammogram_010.jpg',
                'tumor_detected': True,
                'num_detections': 1,
                'max_confidence': 0.91,
                'avg_confidence': 0.91,
                'processing_time': 3.5,
                'annotated_image_path': 'web_annotated_20240920_210000_mammogram_010.jpg',
                'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
                'user_id': 1
            }
        ]
        
        # Insert sample analyses
        for analysis in sample_analyses:
            conn.execute("""
                INSERT INTO analysis_results 
                (image_name, tumor_detected, num_detections, max_confidence, avg_confidence, 
                 processing_time, annotated_image_path, created_at, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis['image_name'],
                analysis['tumor_detected'],
                analysis['num_detections'],
                analysis['max_confidence'],
                analysis['avg_confidence'],
                analysis['processing_time'],
                analysis['annotated_image_path'],
                analysis['created_at'],
                analysis['user_id']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Added {len(sample_analyses)} sample analyses")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add sample data: {e}")
        return False

def add_sample_detections():
    """Add sample detection data"""
    print("🔍 Adding sample detection data...")
    
    try:
        conn = get_db_connection()
        
        # Get analysis IDs
        analyses = conn.execute("SELECT id FROM analysis_results WHERE tumor_detected = 1").fetchall()
        
        if not analyses:
            print("⚠️  No analyses with tumors found")
            return False
        
        # Sample detection data
        sample_detections = [
            # For analysis 1 (2 detections)
            {'result_id': analyses[0]['id'], 'confidence': 0.87, 'x_min': 0.2, 'y_min': 0.3, 'x_max': 0.4, 'y_max': 0.5},
            {'result_id': analyses[0]['id'], 'confidence': 0.57, 'x_min': 0.6, 'y_min': 0.7, 'x_max': 0.8, 'y_max': 0.9},
            
            # For analysis 2 (1 detection)
            {'result_id': analyses[1]['id'], 'confidence': 0.94, 'x_min': 0.1, 'y_min': 0.2, 'x_max': 0.3, 'y_max': 0.4},
            
            # For analysis 3 (3 detections)
            {'result_id': analyses[2]['id'], 'confidence': 0.76, 'x_min': 0.2, 'y_min': 0.3, 'x_max': 0.4, 'y_max': 0.5},
            {'result_id': analyses[2]['id'], 'confidence': 0.68, 'x_min': 0.5, 'y_min': 0.6, 'x_max': 0.7, 'y_max': 0.8},
            {'result_id': analyses[2]['id'], 'confidence': 0.60, 'x_min': 0.1, 'y_min': 0.8, 'x_max': 0.3, 'y_max': 0.9},
            
            # For analysis 4 (1 detection)
            {'result_id': analyses[3]['id'], 'confidence': 0.89, 'x_min': 0.3, 'y_min': 0.4, 'x_max': 0.5, 'y_max': 0.6},
            
            # For analysis 5 (2 detections)
            {'result_id': analyses[4]['id'], 'confidence': 0.82, 'x_min': 0.2, 'y_min': 0.3, 'x_max': 0.4, 'y_max': 0.5},
            {'result_id': analyses[4]['id'], 'confidence': 0.68, 'x_min': 0.6, 'y_min': 0.7, 'x_max': 0.8, 'y_max': 0.9},
            
            # For analysis 6 (1 detection)
            {'result_id': analyses[5]['id'], 'confidence': 0.91, 'x_min': 0.4, 'y_min': 0.5, 'x_max': 0.6, 'y_max': 0.7}
        ]
        
        # Insert sample detections
        for detection in sample_detections:
            conn.execute("""
                INSERT INTO detections 
                (result_id, confidence, x_min, y_min, x_max, y_max)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                detection['result_id'],
                detection['confidence'],
                detection['x_min'],
                detection['y_min'],
                detection['x_max'],
                detection['y_max']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Added {len(sample_detections)} sample detections")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add sample detections: {e}")
        return False

def add_sample_logs():
    """Add sample system logs"""
    print("📝 Adding sample system logs...")
    
    try:
        conn = get_db_connection()
        
        # Sample log data
        sample_logs = [
            ('INFO', 'User admin logged in', 'auth', 1),
            ('INFO', 'Analysis completed for mammogram_001.jpg - Tumor: True', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_002.jpg - Tumor: False', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_003.jpg - Tumor: True', 'analysis', 1),
            ('WARNING', 'Low confidence detection in mammogram_004.jpg', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_005.jpg - Tumor: False', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_006.jpg - Tumor: True', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_007.jpg - Tumor: False', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_008.jpg - Tumor: True', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_009.jpg - Tumor: False', 'analysis', 1),
            ('INFO', 'Analysis completed for mammogram_010.jpg - Tumor: True', 'analysis', 1),
            ('INFO', 'User admin logged out', 'auth', 1)
        ]
        
        # Insert sample logs
        for log in sample_logs:
            conn.execute("""
                INSERT INTO system_logs 
                (level, message, module, user_id)
                VALUES (?, ?, ?, ?)
            """, log)
        
        conn.commit()
        conn.close()
        
        print(f"✅ Added {len(sample_logs)} sample logs")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add sample logs: {e}")
        return False

def main():
    """Main function"""
    print("🔬 OncoVision Sample Data Generator")
    print("=" * 50)
    
    # Check if database exists
    if not Path('oncovision.db').exists():
        print("❌ Database not found. Run: python init_db.py")
        return
    
    # Add sample data
    success = True
    success &= add_sample_analyses()
    success &= add_sample_detections()
    success &= add_sample_logs()
    
    if success:
        print("\n🎉 Sample data added successfully!")
        print("📊 You now have:")
        print("   - 10 sample analyses")
        print("   - Multiple detections")
        print("   - System logs")
        print("\n🚀 Start the app: python app.py")
    else:
        print("\n❌ Some errors occurred while adding sample data")

if __name__ == '__main__':
    main()
