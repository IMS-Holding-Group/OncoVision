#!/usr/bin/env python3
"""
Training script for OncoVision
Trains YOLOv8 model on mammogram data
"""

import os
import sys
import argparse
from pathlib import Path
from ultralytics import YOLO

def train_model(model_size='s', epochs=100, batch_size=16, imgsz=640, device='auto'):
    """Train YOLOv8 model"""
    print("🔬 OncoVision Model Training")
    print("=" * 50)
    
    # Check if data.yaml exists
    if not Path('data.yaml').exists():
        print("❌ data.yaml not found. Run: python prepare_yolo.py")
        return False
    
    # Check if data exists
    data_dir = Path('data/yolo_dataset')
    if not data_dir.exists():
        print("❌ Data directory not found. Run: python prepare_yolo.py")
        return False
    
    # Check for images
    train_images = list((data_dir / 'train' / 'images').glob('*.jpg')) + list((data_dir / 'train' / 'images').glob('*.png'))
    if len(train_images) == 0:
        print("❌ No training images found. Add images to data/yolo_dataset/train/images/")
        return False
    
    print(f"📊 Training data: {len(train_images)} images")
    
    try:
        # Load model
        model_name = f'yolov8{model_size}.pt'
        print(f"🤖 Loading model: {model_name}")
        model = YOLO(model_name)
        
        # Train model
        print(f"🚀 Starting training...")
        print(f"   Model: {model_name}")
        print(f"   Epochs: {epochs}")
        print(f"   Batch size: {batch_size}")
        print(f"   Image size: {imgsz}")
        print(f"   Device: {device}")
        
        results = model.train(
            data='data.yaml',
            epochs=epochs,
            batch=batch_size,
            imgsz=imgsz,
            device=device,
            project='runs',
            name='oncovision_training',
            save=True,
            save_period=10,
            val=True,
            plots=True,
            verbose=True
        )
        
        print("✅ Training completed successfully!")
        
        # Save best model
        best_model_path = 'runs/oncovision_training/weights/best.pt'
        if Path(best_model_path).exists():
            # Copy to models directory
            models_dir = Path('models')
            models_dir.mkdir(exist_ok=True)
            
            shutil.copy2(best_model_path, 'models/oncovision_latest.pt')
            print(f"💾 Best model saved to: models/oncovision_latest.pt")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def main():
    """Main training function"""
    parser = argparse.ArgumentParser(description='Train OncoVision YOLOv8 model')
    parser.add_argument('--model', type=str, default='s', choices=['n', 's', 'm', 'l', 'x'],
                        help='Model size (nano, small, medium, large, extra-large)')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=16,
                        help='Batch size for training')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size for training')
    parser.add_argument('--device', type=str, default='auto',
                        help='Device to use (auto, cpu, 0, 1, etc.)')
    
    args = parser.parse_args()
    
    success = train_model(
        model_size=args.model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        imgsz=args.imgsz,
        device=args.device
    )
    
    if success:
        print("\n🎉 Training completed successfully!")
        print("📁 Check the 'runs' directory for training results")
        print("💾 Best model saved to 'models/oncovision_latest.pt'")
        print("\n🚀 Next steps:")
        print("1. Test the model: python evaluate.py")
        print("2. Run inference: python infer.py --image test.jpg")
        print("3. Start web app: python app.py")
    else:
        print("\n❌ Training failed!")
        print("🔍 Check the error messages above")
        sys.exit(1)

if __name__ == '__main__':
    main()