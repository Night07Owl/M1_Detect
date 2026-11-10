# Deliverable 2: OpenCV Real-Time Pipeline Dossier

**Milestone:** M1 (DETECT)  
**Deliverable ID:** D2 – OpenCV Pipeline  
**Target Object:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure  
**Pipeline Source:** `pipeline/opencv_pipeline.py`  
**Date:** November 10, 2026

---

## 1. Pipeline Capabilities & Design

The real-time OpenCV pipeline provides a deterministic, low-latency video processing loop equipped with telemetry overlays and modular model inference.

### Two Operational Modes:
1. **MODE A (Passthrough Baseline):**
   - Video capture from physical camera (`cv2.CAP_DSHOW` / `cv2.CAP_ANY`)
   - Sensor latency tracking (`PerformanceMonitor`)
   - Real-time Heads-Up Display (HUD) showing frame rate, latency, and 0 detected enclosures
   - Serves as the latency baseline before adding neural network compute.
2. **MODE B (YOLO Enclosure Detection):**
   - Active neural detection of the RMCS-610 assembled housing (`Class ID: 0`, name: `enclosure`)
   - Multi-backend inference engine supporting ONNX Runtime, OpenCV DNN, and Ultralytics
   - Letterbox preprocessing preserving 1:1 geometric aspect ratio
   - Non-Maximum Suppression (NMS) to eliminate duplicate boxes
   - Corner-accented bounding box rendering, confidence percentage, detected count, and latency breakdown.

---

## 2. Evidence Files in this Folder

| File Name | Description | Verification Method |
| :--- | :--- | :--- |
| `mode_a_pipeline.jpg` | Genuine live camera frame with Mode A HUD overlay | Captured via `pipeline/opencv_pipeline.py --mode A` |
| `mode_b_pipeline.jpg` | Live camera frame with Mode B HUD and detector telemetry | Generated via `pipeline/opencv_pipeline.py --mode B` |
| `pipeline_specification.md` | Architecture, data flow, telemetry calculations, and latency breakdown | Source code inspection |
| `demonstration_guide.md` | Interactive demonstration and reproduction instructions | Examiner execution guide |

---

## 3. Real-Time Telemetry Metrics Observed

- **Empirical Video Stream Rate:** ~20.0 FPS
- **Average Frame Acquisition Latency:** ~89.1 ms (DirectShow camera capture)
- **HUD Telemetry Fields:**
  - Pipeline Mode Badge (`MODE A: OPENCV CAMERA PASSTHROUGH` / `MODE B: YOLO ENCLOSURE DETECTOR`)
  - Running FPS
  - Total Processing Latency (ms)
  - Camera Acquisition Latency (ms)
  - Detected Enclosures Count (`Enclosures: N`)
  - Target Object Identifier (`Rhino Motion RMCS-610`)
  - User Control Hotkeys (`[Q] Quit`, `[S] Save Snapshot`)
