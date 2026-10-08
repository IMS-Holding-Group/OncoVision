#!/usr/bin/env python3
"""
OncoVision - Database Update Script
Add missing user_id column to existing database
"""

import sqlite3
import os
from pathlib import Path

def update_database():
    """Update existing database to add user_id column"""
    db_path = Path("oncovision.db")
    
    if not db_path.exists():
        print("❌ Database file not found. Please run init_db.py first.")
        return
    
    print("🔄 Updating OncoVision Database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if user_id column exists
        cursor.execute("PRAGMA table_info(analysis_results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("➕ Adding user_id column to analysis_results table...")
            
            # Add user_id column with default value 1 (admin user)
            cursor.execute("""
                ALTER TABLE analysis_results 
                ADD COLUMN user_id INTEGER DEFAULT 1
            """)
            
            # Update existing records to have user_id = 1
            cursor.execute("""
                UPDATE analysis_results 
                SET user_id = 1 
                WHERE user_id IS NULL
            """)
            
            print("✅ user_id column added successfully")
        else:
            print("✅ user_id column already exists")
        
        # Ensure admin user exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            print("➕ Creating admin user...")
            import hashlib
            password_hash = hashlib.sha256("".encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, ("admin", "admin@oncovision.com", password_hash, "admin"))
            
            print("✅ Admin user created")
        else:
            print("✅ Admin user already exists")
        
        conn.commit()
        print("✅ Database update completed successfully!")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()
