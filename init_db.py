#!/usr/bin/env python3
"""
Database initialization script for OncoVision
Creates the database and tables if they don't exist
"""

import sqlite3
import hashlib
from pathlib import Path

def get_db_connection():
    """Get database connection with proper timeout and WAL mode"""
    conn = sqlite3.connect('oncovision.db', timeout=30.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    # Set busy timeout
    conn.execute("PRAGMA busy_timeout=30000")
    return conn

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize database with proper schema"""
    try:
        conn = get_db_connection()
        
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
        
        # Create default admin user if it doesn't exist
        admin_exists = conn.execute(
            'SELECT COUNT(*) FROM users WHERE username = ?', ('admin',)
        ).fetchone()[0]
        
        if admin_exists == 0:
            admin_password = hash_password('admin123')
            conn.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, ('admin', admin_password, 'admin'))
            print("✅ Default admin user created (username: admin, password: admin123)")
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🔬 OncoVision Database Initialization")
    print("=" * 50)
    
    if init_database():
        print("🎉 Database setup completed successfully!")
        print("📝 Default admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("⚠️  Please change the default password after first login!")
    else:
        print("❌ Database setup failed!")
        exit(1)