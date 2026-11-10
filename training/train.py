"""
YOLO Training Pipeline for Single-Class Enclosure Detection
Trains YOLOv8n/v11n architecture on the RMCS-610 dataset and exports to ONNX.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import glob
import argparse
import json
import shutil

def run_training(data_yaml="dataset/dataset.yaml", epochs=50, imgsz=640, batch=16,
                 weights="yolov8n.pt", device=None, output_dir="models"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Audit Training Images
    train_imgs = glob.glob("dataset/images/train/*.*")
    if len(train_imgs) == 0:
        msg = (
            "[!] STATUS: PENDING DATA\n"
            "Zero training images found in 'dataset/images/train/'.\n"
            "To train the detector:\n"
            "  1. Capture real photographs of your physical RMCS-610 controller.\n"
            "  2. Place them in 'dataset/images/' and run 'python dataset/annotate_dataset.py'.\n"
            "  3. Run 'python dataset/split_dataset.py' to generate the 70/20/10 split.\n"
            "  4. Re-run 'python training/train.py'."
        )
        print(msg)
        status_file = os.path.join("06_train_and_run_detector", "training_status.json")
        os.makedirs(os.path.dirname(status_file), exist_ok=True)
        with open(status_file, "w") as f:
            json.dump({
                "status": "PENDING_DATA",
                "message": "Awaiting physical photographs and annotations.",
                "training_images_count": 0
            }, f, indent=2)
        return False
        
    print(f"[+] Found {len(train_imgs)} verified training images. Initializing training...")
    
    try:
        from ultralytics import YOLO
        import torch
        
        # Select device
        if device is None:
            device = "0" if torch.cuda.is_available() else "cpu"
        print(f"[+] Training on device: {device}")
        
        model = YOLO(weights)
        results = model.train(
            data=os.path.abspath(data_yaml),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            device=device,
            name="rmcs610_enclosure",
            project="runs/detect",
            exist_ok=True,
            single_cls=True,
            verbose=True
        )
        
        # Save best PyTorch weights
        best_pt = os.path.join("runs", "detect", "rmcs610_enclosure", "weights", "best.pt")
        target_pt = os.path.join(output_dir, "enclosure_yolo.pt")
        if os.path.exists(best_pt):
            shutil.copy(best_pt, target_pt)
            print(f"[+] Copied best PyTorch weights to: {target_pt}")
            
            # Export to ONNX for Edge AI deployment
            print("[+] Exporting trained model to ONNX format (opset 17)...")
            trained_model = YOLO(target_pt)
            onnx_path = trained_model.export(format="onnx", opset=17, imgsz=imgsz)
            target_onnx = os.path.join(output_dir, "enclosure_yolo.onnx")
            shutil.copy(onnx_path, target_onnx)
            print(f"[+] Exported Edge AI ONNX model: {target_onnx}")
            
        return True
        
    except Exception as e:
        print(f"[-] Training halted: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLO RMCS-610 Enclosure Detector")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Image resolution")
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="Base pretrained weights")
    parser.add_argument("--device", type=str, default=None, help="Device (0 or cpu)")
    
    args = parser.parse_args()
    run_training(epochs=args.epochs, batch=args.batch, imgsz=args.imgsz,
                 weights=args.weights, device=args.device)

