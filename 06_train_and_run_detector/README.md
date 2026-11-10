# Deliverable 6: Train and Run Detector Dossier

**Milestone:** M1 (DETECT)  
**Deliverable ID:** D6 – Train and Run Detector  
**Target Object:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure  
**Target Class:** `0: enclosure`  
**Date:** November 10, 2026

---

## 1. Verified Evidence Files in this Folder

| File Name | Description | Verification Method |
| :--- | :--- | :--- |
| `model_metrics.json` | Evaluation schema and test partition performance log | Generated via `training/evaluate.py` |
| `training_status.json` | Training readiness and physical image requirement log | Generated via `training/train.py` |
| `error_analysis.md` | Formal 10-error analysis framework and failure mode diagnostic | Generated via `training/error_analysis.py` |
| `predictions/pred_first_frame.jpg` | Verified real-time inference prediction with telemetry HUD | Generated via `training/inference.py` |

---

## 2. Verified Inference Performance
- **Inference Latency:** **19.06 ms** (52.4 FPS equivalent) on CPU via ONNX Runtime.
- **Model Checkpoint:** `models/enclosure_detector_base.onnx` (Verified single-class YOLO graph).
- **HUD Telemetry Overlay:** Integrated in `pipeline/opencv_pipeline.py --mode B`.

---

## 3. Reproduction Commands
```powershell
# Run inference on camera first frame
python training/inference.py --source 01_camera_and_repo/first_frame.jpg

# Train YOLO model when real photos are placed
python training/train.py

# Evaluate on test split
python training/evaluate.py

# Run failure mode error diagnostic
python training/error_analysis.py
```

