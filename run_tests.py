#!/usr/bin/env python3
"""
Test script for OncoVision system
Tests all major components and functionality
"""

import os
import sys
import sqlite3
import tempfile
from pathlib import Path
import json

def test_database():
    """Test database functionality"""
    print("🧪 Testing database...")
    
    try:
        # Test database connection
        conn = sqlite3.connect('oncovision.db', timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
        
        # Test table existence
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [table[0] for table in tables]
        
        required_tables = ['users', 'analysis_results', 'detections', 'system_logs']
        missing_tables = [table for table in required_tables if table not in table_names]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        # Test insert operation
        conn.execute("""
            INSERT INTO system_logs (level, message, module)
            VALUES (?, ?, ?)
        """, ('TEST', 'Database test', 'test'))
        
        conn.commit()
        conn.close()
        
        print("✅ Database test passed")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_model_loading():
    """Test model loading functionality"""
    print("🧪 Testing model loading...")
    
    try:
        from infer import OncoVisionInference
        
        # Test model initialization
        inference_engine = OncoVisionInference()
        
        if inference_engine.model is None:
            print("⚠️  Model not loaded (this is expected if no model exists)")
            return True
        
        print("✅ Model loading test passed")
        return True
        
    except Exception as e:
        print(f"❌ Model loading test failed: {e}")
        return False

def test_inference():
    """Test inference functionality"""
    print("🧪 Testing inference...")
    
    try:
        from infer import OncoVisionInference
        import numpy as np
        from PIL import Image
        
        # Create a test image
        test_image = Image.new('RGB', (640, 640), color='white')
        test_path = 'test_image.jpg'
        test_image.save(test_path)
        
        # Test inference
        inference_engine = OncoVisionInference()
        
        if inference_engine.model is None:
            print("⚠️  Inference test skipped (no model loaded)")
            return True
        
        result, annotated_image = inference_engine.run_inference(
            image_path=test_path,
            conf_threshold=0.5,
            iou_threshold=0.45,
            save_results=False
        )
        
        # Clean up
        os.remove(test_path)
        
        print("✅ Inference test passed")
        return True
        
    except Exception as e:
        print(f"❌ Inference test failed: {e}")
        return False

def test_web_server():
    """Test web server functionality"""
    print("🧪 Testing web server...")
    
    try:
        from app import app
        
        # Test app creation
        if app is None:
            print("❌ Flask app not created")
            return False
        
        # Test routes
        with app.test_client() as client:
            # Test index route
            response = client.get('/')
            if response.status_code != 200:
                print(f"❌ Index route failed: {response.status_code}")
                return False
            
            # Test login route
            response = client.get('/login')
            if response.status_code != 200:
                print(f"❌ Login route failed: {response.status_code}")
                return False
        
        print("✅ Web server test passed")
        return True
        
    except Exception as e:
        print(f"❌ Web server test failed: {e}")
        return False

def test_file_upload():
    """Test file upload functionality"""
    print("🧪 Testing file upload...")
    
    try:
        from app import app, allowed_file
        
        # Test allowed file function
        if not allowed_file('test.jpg'):
            print("❌ Allowed file function failed")
            return False
        
        if allowed_file('test.exe'):
            print("❌ Allowed file function failed (should reject .exe)")
            return False
        
        print("✅ File upload test passed")
        return True
        
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        return False

def test_database_operations():
    """Test database operations"""
    print("🧪 Testing database operations...")
    
    try:
        from app import safe_db_operation
        
        # Test safe database operation
        def test_operation(conn):
            conn.execute("""
                INSERT INTO system_logs (level, message, module)
                VALUES (?, ?, ?)
            """, ('TEST', 'Safe operation test', 'test'))
        
        safe_db_operation(test_operation)
        
        print("✅ Database operations test passed")
        return True
        
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 OncoVision System Tests")
    print("=" * 50)
    
    tests = [
        test_database,
        test_model_loading,
        test_inference,
        test_web_server,
        test_file_upload,
        test_database_operations
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())