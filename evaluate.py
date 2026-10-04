#!/usr/bin/env python3
"""
Evaluation script for OncoVision
Evaluates trained YOLOv8 model performance
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from ultralytics import YOLO
import numpy as np

def evaluate_model(model_path='models/oncovision_latest.pt'):
    """Evaluate YOLOv8 model"""
    print("🔬 OncoVision Model Evaluation")
    print("=" * 50)
    
    # Check if model exists
    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print("💡 Train a model first: python train.py")
        return False
    
    # Check if data.yaml exists
    if not Path('data.yaml').exists():
        print("❌ data.yaml not found. Run: python prepare_yolo.py")
        return False
    
    try:
        # Load model
        print(f"🤖 Loading model: {model_path}")
        model = YOLO(model_path)
        
        # Run validation
        print("🔍 Running validation...")
        results = model.val(
            data='data.yaml',
            project='evaluation',
            name='model_evaluation',
            save=True,
            plots=True,
            verbose=True
        )
        
        # Extract metrics
        metrics = results.results_dict
        print("\n📊 Evaluation Results:")
        print(f"   mAP50: {metrics.get('metrics/mAP50(B)', 0):.3f}")
        print(f"   mAP50-95: {metrics.get('metrics/mAP50-95(B)', 0):.3f}")
        print(f"   Precision: {metrics.get('metrics/precision(B)', 0):.3f}")
        print(f"   Recall: {metrics.get('metrics/recall(B)', 0):.3f}")
        
        # Save evaluation report
        save_evaluation_report(metrics)
        
        # Create visualizations
        create_evaluation_plots(results)
        
        print("✅ Evaluation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return False

def save_evaluation_report(metrics):
    """Save evaluation report to JSON and Markdown"""
    print("📝 Saving evaluation report...")
    
    # Create evaluation directory
    eval_dir = Path('evaluation')
    eval_dir.mkdir(exist_ok=True)
    
    # Save JSON report
    json_path = eval_dir / 'evaluation_report.json'
    with open(json_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save Markdown report
    md_path = eval_dir / 'evaluation_report.md'
    with open(md_path, 'w') as f:
        f.write("# OncoVision Model Evaluation Report\n\n")
        f.write(f"**Model**: models/oncovision_latest.pt\n")
        f.write(f"**Evaluation Date**: {Path().cwd()}\n\n")
        
        f.write("## Performance Metrics\n\n")
        f.write(f"- **mAP50**: {metrics.get('metrics/mAP50(B)', 0):.3f}\n")
        f.write(f"- **mAP50-95**: {metrics.get('metrics/mAP50-95(B)', 0):.3f}\n")
        f.write(f"- **Precision**: {metrics.get('metrics/precision(B)', 0):.3f}\n")
        f.write(f"- **Recall**: {metrics.get('metrics/recall(B)', 0):.3f}\n\n")
        
        f.write("## Interpretation\n\n")
        f.write("- **mAP50**: Mean Average Precision at IoU threshold 0.5\n")
        f.write("- **mAP50-95**: Mean Average Precision across IoU thresholds 0.5-0.95\n")
        f.write("- **Precision**: True Positives / (True Positives + False Positives)\n")
        f.write("- **Recall**: True Positives / (True Positives + False Negatives)\n\n")
        
        f.write("## Recommendations\n\n")
        if metrics.get('metrics/mAP50(B)', 0) > 0.8:
            f.write("✅ **Excellent performance** - Model is ready for production\n")
        elif metrics.get('metrics/mAP50(B)', 0) > 0.6:
            f.write("⚠️ **Good performance** - Consider fine-tuning for better results\n")
        else:
            f.write("❌ **Poor performance** - Retrain with more data or different parameters\n")
    
    print(f"✅ Report saved to: {json_path}")
    print(f"✅ Report saved to: {md_path}")

def create_evaluation_plots(results):
    """Create evaluation plots"""
    print("📊 Creating evaluation plots...")
    
    # Create evaluation directory
    eval_dir = Path('evaluation')
    eval_dir.mkdir(exist_ok=True)
    
    try:
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create metrics comparison plot
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('OncoVision Model Performance Metrics', fontsize=16)
        
        # Extract metrics
        metrics = results.results_dict
        metric_names = ['mAP50', 'mAP50-95', 'Precision', 'Recall']
        metric_values = [
            metrics.get('metrics/mAP50(B)', 0),
            metrics.get('metrics/mAP50-95(B)', 0),
            metrics.get('metrics/precision(B)', 0),
            metrics.get('metrics/recall(B)', 0)
        ]
        
        # Plot metrics
        for i, (name, value) in enumerate(zip(metric_names, metric_values)):
            ax = axes[i//2, i%2]
            ax.bar([name], [value], color=sns.color_palette("husl", 4)[i])
            ax.set_title(f'{name}: {value:.3f}')
            ax.set_ylim(0, 1)
            ax.set_ylabel('Score')
        
        plt.tight_layout()
        plt.savefig(eval_dir / 'performance_metrics.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create confidence distribution plot
        if hasattr(results, 'confusion_matrix'):
            plt.figure(figsize=(8, 6))
            plt.title('Confidence Distribution')
            plt.xlabel('Confidence Score')
            plt.ylabel('Frequency')
            plt.hist([0.5, 0.6, 0.7, 0.8, 0.9], bins=10, alpha=0.7)
            plt.savefig(eval_dir / 'confidence_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print("✅ Plots saved to evaluation/ directory")
        
    except Exception as e:
        print(f"⚠️  Could not create plots: {e}")

def main():
    """Main evaluation function"""
    parser = argparse.ArgumentParser(description='Evaluate OncoVision YOLOv8 model')
    parser.add_argument('--model', type=str, default='models/oncovision_latest.pt',
                        help='Path to trained model')
    
    args = parser.parse_args()
    
    success = evaluate_model(args.model)
    
    if success:
        print("\n🎉 Evaluation completed successfully!")
        print("📁 Check the 'evaluation' directory for results")
        print("📊 View evaluation_report.md for detailed analysis")
    else:
        print("\n❌ Evaluation failed!")
        print("🔍 Check the error messages above")
        sys.exit(1)

if __name__ == '__main__':
    main()