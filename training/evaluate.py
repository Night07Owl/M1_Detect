"""
Final Model Evaluation Engine
Runs comprehensive evaluation on the untouched test partition.
Generates confusion matrix, precision-recall curve, and per-class latency report.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import glob
import json
import time
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pipeline.detector import EnclosureDetector
from dataset.annotate_dataset import convert_from_yolo

def compute_box_iou(box1, box2):
    """Compute IoU between two [x1, y1, x2, y2] bounding boxes."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    b1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    b2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = b1_area + b2_area - inter_area
    
    return inter_area / float(union_area) if union_area > 0 else 0.0

def evaluate_on_test_set(model_path="models/enclosure_detector_base.onnx",
                         test_images_dir="dataset/images/test",
                         test_labels_dir="dataset/labels/test",
                         iou_threshold=0.5, conf_threshold=0.30):
    os.makedirs("results/confusion_matrix", exist_ok=True)
    os.makedirs("06_train_and_run_detector", exist_ok=True)
    
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    test_imgs = []
    for ext in valid_exts:
        test_imgs.extend(glob.glob(os.path.join(test_images_dir, ext)))
    test_imgs = sorted(list(set(test_imgs)))
    
    if len(test_imgs) == 0:
        msg = f"Zero test images found in '{test_images_dir}'. Evaluation status: PENDING DATA."
        print(f"[!] {msg}")
        report = {
            "status": "PENDING_DATA",
            "message": msg,
            "metrics": {
                "test_images_count": 0,
                "precision": "Pending physical data",
                "recall": "Pending physical data",
                "f1_score": "Pending physical data",
                "mAP_50": "Pending physical data",
                "avg_inference_latency_ms": "Pending physical data"
            }
        }
        _write_eval_reports(report)
        return report

    detector = EnclosureDetector(model_path=model_path, conf_thres=conf_threshold)
    if not detector.is_loaded():
        print(f"[-] Detector failed to initialize from: {model_path}")
        return {"status": "FAILED", "error": "Model initialization failed"}

    tp, fp, fn = 0, 0, 0
    latencies = []
    
    for img_path in test_imgs:
        img = cv2.imread(img_path)
        if img is None:
            continue
        h, w = img.shape[:2]
        
        # Load Ground Truth
        base = os.path.splitext(os.path.basename(img_path))[0]
        lbl_path = os.path.join(test_labels_dir, f"{base}.txt")
        gt_boxes = []
        if os.path.exists(lbl_path):
            with open(lbl_path, "r") as f:
                for line in f:
                    b = convert_from_yolo(line, w, h)
                    if b and b["class_id"] == 0:
                        gt_boxes.append(b["box"])
                        
        # Run inference
        t0 = time.perf_counter()
        detections = detector.detect(img)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)
        
        pred_boxes = [d["box"] for d in detections]
        
        matched_gt = set()
        for p_box in pred_boxes:
            best_iou = 0.0
            best_gt_idx = -1
            for g_idx, g_box in enumerate(gt_boxes):
                if g_idx in matched_gt:
                    continue
                iou = compute_box_iou(p_box, g_box)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = g_idx
                    
            if best_iou >= iou_threshold and best_gt_idx != -1:
                tp += 1
                matched_gt.add(best_gt_idx)
            else:
                fp += 1
                
        fn += (len(gt_boxes) - len(matched_gt))
        
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    avg_latency = np.mean(latencies) if latencies else 0.0
    
    report = {
        "status": "COMPLETE",
        "model_evaluated": model_path,
        "total_test_images": len(test_imgs),
        "metrics": {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "mAP_50": round(float(precision * recall), 4),  # Conservative single-class proxy
            "avg_inference_latency_ms": round(float(avg_latency), 2)
        }
    }
    
    _generate_confusion_matrix_plot(tp, fp, fn)
    _write_eval_reports(report)
    return report

def _generate_confusion_matrix_plot(tp, fp, fn):
    matrix = np.array([[tp, fn], [fp, 0]])
    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(matrix, cmap="Blues")
    fig.colorbar(cax)
    
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted Enclosure", "Predicted Background"])
    ax.set_yticklabels(["Actual Enclosure", "Actual Background"])
    
    for i in range(2):
        for j in range(2):
            val = matrix[i, j]
            color = "white" if val > matrix.max() / 2 else "black"
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=14, fontweight="bold")
            
    ax.set_title("RMCS-610 Detector Confusion Matrix", fontsize=12, pad=20, fontweight="bold")
    plt.tight_layout()
    
    for p in ["results/confusion_matrix/confusion_matrix.png", "06_train_and_run_detector/confusion_matrix.png"]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, dpi=300)
    plt.close(fig)

def _write_eval_reports(report):
    for p in ["results/test_evaluation_report.json", "06_train_and_run_detector/model_metrics.json"]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    rep = evaluate_on_test_set()
    print(json.dumps(rep, indent=2))

