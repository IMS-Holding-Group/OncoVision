#!/usr/bin/env python3
"""
Inference script for OncoVision
Performs tumor detection on mammogram images
"""

import os
import sys
import argparse
import json
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class OncoVisionInference:
    """OncoVision inference engine"""
    
    def __init__(self, model_path='models/oncovision_latest.pt'):
        """Initialize inference engine"""
        self.model_path = model_path
        self.model = None
        
        # Try to load model
        if Path(model_path).exists():
            try:
                self.model = YOLO(model_path)
                print(f"✅ Model loaded: {model_path}")
            except Exception as e:
                print(f"⚠️  Could not load model: {e}")
        else:
            print(f"⚠️  Model not found: {model_path}")
            print("💡 Train a model first: python train.py")
    
    def run_inference(self, image_path, conf_threshold=0.5, iou_threshold=0.45, save_results=True):
        """Run inference on image"""
        if self.model is None:
            return self._mock_result(), None
        
        try:
            # Run inference
            results = self.model(
                image_path,
                conf=conf_threshold,
                iou=iou_threshold,
                save=False,
                verbose=False
            )
            
            # Process results
            result = results[0]
            boxes = result.boxes
            
            # Extract detections
            detections = []
            if boxes is not None:
                for box in boxes:
                    detection = {
                        'confidence': float(box.conf[0]),
                        'bbox': box.xyxy[0].tolist(),
                        'class': int(box.cls[0])
                    }
                    detections.append(detection)
            
            # Create summary
            summary = {
                'tumor_detected': len(detections) > 0,
                'num_detections': len(detections),
                'max_confidence': max([d['confidence'] for d in detections]) if detections else 0.0,
                'avg_confidence': np.mean([d['confidence'] for d in detections]) if detections else 0.0
            }
            
            # Create annotated image
            annotated_image = self._create_annotated_image(image_path, detections)
            
            # Save results if requested
            if save_results:
                self._save_results(image_path, detections, summary, annotated_image)
            
            return {
                'summary': summary,
                'predictions': detections
            }, annotated_image
            
        except Exception as e:
            print(f"❌ Inference failed: {e}")
            return self._mock_result(), None
    
    def _mock_result(self):
        """Return mock result when model is not available"""
        return {
            'summary': {
                'tumor_detected': False,
                'num_detections': 0,
                'max_confidence': 0.0,
                'avg_confidence': 0.0
            },
            'predictions': []
        }
    
    def _create_annotated_image(self, image_path, detections):
        """Create annotated image with bounding boxes"""
        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            return None
        
        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Draw bounding boxes
        for detection in detections:
            bbox = detection['bbox']
            confidence = detection['confidence']
            
            # Convert normalized coordinates to pixel coordinates
            h, w = image_rgb.shape[:2]
            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            
            # Draw rectangle
            cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
            
            # Draw confidence
            label = f"Tumor: {confidence:.2f}"
            cv2.putText(image_rgb, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        return image_rgb
    
    def _save_results(self, image_path, detections, summary, annotated_image):
        """Save inference results"""
        # Create results directory
        results_dir = Path('inference_results')
        results_dir.mkdir(exist_ok=True)
        
        # Generate filenames
        base_name = Path(image_path).stem
        timestamp = Path(image_path).name.split('_')[0] if '_' in Path(image_path).name else 'unknown'
        
        # Save annotated image
        if annotated_image is not None:
            annotated_path = results_dir / f"annotated_{base_name}.jpg"
            annotated_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(annotated_path), annotated_bgr)
            print(f"🖼️  Annotated image saved: {annotated_path}")
        
        # Save JSON results
        json_path = results_dir / f"result_{base_name}.json"
        result_data = {
            'image_path': str(image_path),
            'summary': summary,
            'detections': detections,
            'timestamp': timestamp
        }
        
        with open(json_path, 'w') as f:
            json.dump(result_data, f, indent=2)
        print(f"📄 JSON result saved: {json_path}")

def main():
    """Main inference function"""
    parser = argparse.ArgumentParser(description='Run OncoVision inference')
    parser.add_argument('--image', type=str, required=True,
                        help='Path to image or directory of images')
    parser.add_argument('--model', type=str, default='models/oncovision_latest.pt',
                        help='Path to trained model')
    parser.add_argument('--conf-threshold', type=float, default=0.5,
                        help='Confidence threshold')
    parser.add_argument('--iou-threshold', type=float, default=0.45,
                        help='IoU threshold')
    parser.add_argument('--batch', action='store_true',
                        help='Process directory of images')
    parser.add_argument('--visualize', action='store_true',
                        help='Show results visually')
    
    args = parser.parse_args()
    
    # Initialize inference engine
    inference_engine = OncoVisionInference(args.model)
    
    if args.batch:
        # Process directory
        image_dir = Path(args.image)
        if not image_dir.exists():
            print(f"❌ Directory not found: {image_dir}")
            sys.exit(1)
        
        image_files = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png'))
        if not image_files:
            print(f"❌ No images found in: {image_dir}")
            sys.exit(1)
        
        print(f"🔍 Processing {len(image_files)} images...")
        
        for image_file in image_files:
            print(f"\n📸 Processing: {image_file.name}")
            result, annotated_image = inference_engine.run_inference(
                image_file,
                conf_threshold=args.conf_threshold,
                iou_threshold=args.iou_threshold,
                save_results=True
            )
            
            print(f"   Tumor detected: {result['summary']['tumor_detected']}")
            print(f"   Detections: {result['summary']['num_detections']}")
            print(f"   Max confidence: {result['summary']['max_confidence']:.3f}")
    
    else:
        # Process single image
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"❌ Image not found: {image_path}")
            sys.exit(1)
        
        print(f"🔍 Processing: {image_path.name}")
        
        result, annotated_image = inference_engine.run_inference(
            image_path,
            conf_threshold=args.conf_threshold,
            iou_threshold=args.iou_threshold,
            save_results=True
        )
        
        print(f"\n📊 Results:")
        print(f"   Tumor detected: {result['summary']['tumor_detected']}")
        print(f"   Number of detections: {result['summary']['num_detections']}")
        print(f"   Max confidence: {result['summary']['max_confidence']:.3f}")
        print(f"   Average confidence: {result['summary']['avg_confidence']:.3f}")
        
        if args.visualize and annotated_image is not None:
            plt.figure(figsize=(12, 8))
            plt.imshow(annotated_image)
            plt.title(f"OncoVision Analysis: {image_path.name}")
            plt.axis('off')
            plt.show()

if __name__ == '__main__':
    main()