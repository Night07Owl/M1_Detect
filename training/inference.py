"""
Enclosure Detector Inference Engine
Runs single-class object detection on images, directories, or camera frames.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import glob
import time
import argparse
import json
import cv2

from pipeline.detector import EnclosureDetector
from pipeline.visualization import draw_detections, draw_hud

def run_inference(model_path="models/enclosure_detector_base.onnx", source="01_camera_and_repo/first_frame.jpg",
                  conf_thres=0.30, save_dir="results/predictions"):
    os.makedirs(save_dir, exist_ok=True)
    evidence_dir = os.path.join("06_train_and_run_detector", "predictions")
    os.makedirs(evidence_dir, exist_ok=True)
    
    print("=" * 60)
    print("ENCLOSURE DETECTOR INFERENCE")
    print(f"Model: {model_path}")
    print(f"Source: {source}")
    print("=" * 60)
    
    detector = EnclosureDetector(model_path=model_path, conf_thres=conf_thres)
    if not detector.is_loaded():
        print(f"[-] Detector failed to load from: {model_path}")
        return []
        
    # Gather image files
    if os.path.isdir(source):
        valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
        image_paths = []
        for ext in valid_exts:
            image_paths.extend(glob.glob(os.path.join(source, ext)))
    elif os.path.isfile(source):
        image_paths = [source]
    else:
        print(f"[-] Source path not found: {source}")
        return []
        
    results_summary = []
    
    for img_path in sorted(image_paths):
        frame = cv2.imread(img_path)
        if frame is None:
            continue
            
        t0 = time.perf_counter()
        detections = detector.detect(frame)
        t1 = time.perf_counter()
        
        latency_ms = (t1 - t0) * 1000.0
        
        # Draw detections
        annotated = frame.copy()
        if detections:
            annotated = draw_detections(annotated, detections)
            
        annotated = draw_hud(
            annotated,
            mode="B",
            fps=1000.0 / latency_ms if latency_ms > 0 else 0.0,
            latency_ms=latency_ms,
            enclosure_count=len(detections)
        )
        
        fname = os.path.basename(img_path)
        out_path = os.path.join(save_dir, f"pred_{fname}")
        evidence_path = os.path.join(evidence_dir, f"pred_{fname}")
        cv2.imwrite(out_path, annotated)
        cv2.imwrite(evidence_path, annotated)
        
        info = {
            "image": fname,
            "latency_ms": round(latency_ms, 2),
            "enclosures_detected": len(detections),
            "detections": detections,
            "output_saved": out_path
        }
        results_summary.append(info)
        print(f"[+] Processed {fname}: {len(detections)} enclosures detected ({latency_ms:.2f} ms)")
        
    # Save inference log
    log_path = os.path.join(save_dir, "inference_log.json")
    with open(log_path, "w") as f:
        json.dump(results_summary, f, indent=2)
    print(f"[+] Inference log saved to: {log_path}")
    
    return results_summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Enclosure Inference")
    parser.add_argument("--model", type=str, default="models/enclosure_detector_base.onnx", help="Model path")
    parser.add_argument("--source", type=str, default="01_camera_and_repo/first_frame.jpg", help="Source file or directory")
    parser.add_argument("--conf", type=float, default=0.30, help="Confidence threshold")
    parser.add_argument("--save-dir", type=str, default="results/predictions", help="Output directory")
    
    args = parser.parse_args()
    run_inference(model_path=args.model, source=args.source, conf_thres=args.conf, save_dir=args.save_dir)

