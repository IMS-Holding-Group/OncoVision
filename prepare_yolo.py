#!/usr/bin/env python3
"""
Data preparation script for OncoVision
Prepares data for YOLOv8 training
"""

import os
import sys
import yaml
import shutil
from pathlib import Path
import json

def create_data_yaml():
    """Create data.yaml file for YOLOv8"""
    data_config = {
        'path': str(Path.cwd() / 'data' / 'yolo_dataset'),
        'train': 'train/images',
        'val': 'val/images',
        'test': 'test/images',
        'nc': 1,  # Number of classes
        'names': ['tumor']  # Class names
    }
    
    with open('data.yaml', 'w') as f:
        yaml.dump(data_config, f, default_flow_style=False)
    
    print("✅ Created data.yaml")

def create_sample_data():
    """Create sample data structure"""
    print("📁 Creating sample data structure...")
    
    # Create directories
    base_dir = Path('data/yolo_dataset')
    dirs = [
        'train/images', 'train/labels',
        'val/images', 'val/labels',
        'test/images', 'test/labels'
    ]
    
    for dir_path in dirs:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    sample_files = [
        'train/images/sample1.jpg',
        'train/labels/sample1.txt',
        'val/images/sample2.jpg',
        'val/labels/sample2.txt',
        'test/images/sample3.jpg',
        'test/labels/sample3.txt'
    ]
    
    for file_path in sample_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch()
    
    print("✅ Sample data structure created")

def download_roboflow_data():
    """Download data from Roboflow (if API key provided)"""
    print("🌐 Roboflow integration...")
    
    api_key = input("Enter Roboflow API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  Skipping Roboflow download")
        return
    
    try:
        from roboflow import Roboflow
        
        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project("mammogram-tumor-detection")
        dataset = project.version(1).download("yolov8")
        
        print("✅ Roboflow data downloaded")
        
    except ImportError:
        print("❌ Roboflow not installed. Install with: pip install roboflow")
    except Exception as e:
        print(f"❌ Roboflow download failed: {e}")

def validate_data():
    """Validate data structure"""
    print("🔍 Validating data structure...")
    
    base_dir = Path('data/yolo_dataset')
    
    # Check required directories
    required_dirs = [
        'train/images', 'train/labels',
        'val/images', 'val/labels',
        'test/images', 'test/labels'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not (base_dir / dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    # Check for images and labels
    for split in ['train', 'val', 'test']:
        images_dir = base_dir / split / 'images'
        labels_dir = base_dir / split / 'labels'
        
        image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
        label_files = list(labels_dir.glob('*.txt'))
        
        if len(image_files) == 0:
            print(f"⚠️  No images found in {split}/images")
        if len(label_files) == 0:
            print(f"⚠️  No labels found in {split}/labels")
    
    print("✅ Data validation completed")
    return True

def main():
    """Main data preparation function"""
    print("🔬 OncoVision Data Preparation")
    print("=" * 50)
    
    # Create data.yaml
    create_data_yaml()
    
    # Create sample data structure
    create_sample_data()
    
    # Try to download from Roboflow
    download_roboflow_data()
    
    # Validate data
    validate_data()
    
    print("\n" + "=" * 50)
    print("📝 Next steps:")
    print("1. Add your mammogram images to data/yolo_dataset/train/images/")
    print("2. Create corresponding label files in data/yolo_dataset/train/labels/")
    print("3. Repeat for val/ and test/ directories")
    print("4. Run: python train.py")
    
    print("\n📖 Label format (YOLO):")
    print("class_id center_x center_y width height")
    print("Example: 0 0.5 0.5 0.3 0.3")
    print("(All values normalized between 0 and 1)")

if __name__ == '__main__':
    main()