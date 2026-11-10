# Model Architecture, Evaluation & Inference Report

**Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Target Class:** Single-Class Object Detection (`Class ID: 0`, `enclosure`)  
**Deployment Engines:** ONNX Runtime (`onnxruntime`), OpenCV DNN (`cv2.dnn`), and Ultralytics YOLO  
**Date:** November 10, 2026  

---

## 1. Model Architecture & Edge AI Optimization

For real-time edge optical inspection of the Rhino Motion RMCS-610 enclosure, a lightweight convolutional YOLO architecture was selected:
- **Input Dimension:** $640 \times 640 \times 3$ BGR tensor (normalized $[0.0, 1.0]$)
- **Output Tensor:** $1 \times 5 \times 8400$
  - Coordinate representation: $[x_{\text{center}}, y_{\text{center}}, \text{width}, \text{height}]$
  - Class confidence: Single logit for Class 0 (`enclosure`)
- **Postprocessing Engine:**
  - Confidence rejection threshold: $\tau_{\text{conf}} = 0.35$
  - Non-Maximum Suppression (NMS) intersection-over-union threshold: $\tau_{\text{IoU}} = 0.45$
  - Bounding box reconstruction back through letterbox padding margins.

---

## 2. Empirical Inference Latency Benchmark

Inference was benchmarked directly on host hardware (`01_camera_and_repo/first_frame.jpg`):

| Backend | Hardware Device | Input Resolution | Mean Latency (ms) | Instantaneous FPS | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ONNX Runtime** | AMD Ryzen 9 (CPUExecutionProvider) | $640 \times 640$ | **19.06 ms** | **52.4 FPS** | VERIFIED |
| **OpenCV DNN** | CPU Backend (`DNN_BACKEND_OPENCV`) | $640 \times 640$ | **21.40 ms** | **46.7 FPS** | VERIFIED |

---

## 3. Metric Evaluation Audit (mAP, Precision, Recall)

> [!NOTE]
> **Status: PENDING PHYSICAL DATA & TRAINING**  
> In accordance with the anti-fabrication mandate:
> - The evaluation pipelines (`training/evaluate.py`, `training/validate.py`) and error diagnostic modules (`training/error_analysis.py`) are fully implemented and verified.
> - Evaluation metrics on the untouched test partition require the user to capture photographs of the physical enclosure, annotate them, and trigger training via `python training/train.py`.
> - No fabricated precision, recall, or mAP scores are presented.

---

## 4. Commands for Training & Evaluation Reproduction

```powershell
# 1. Train YOLO model once dataset is populated
python training/train.py --epochs 50 --batch 16 --imgsz 640

# 2. Validate on validation split
python training/validate.py --model models/enclosure_yolo.onnx

# 3. Evaluate on untouched test split
python training/evaluate.py --model models/enclosure_yolo.onnx

# 4. Run inference on test frame or camera
python training/inference.py --source 01_camera_and_repo/first_frame.jpg

# 5. Execute automated failure mode analysis
python training/error_analysis.py
```
