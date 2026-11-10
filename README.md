# Rhino Motion RMCS-610 Speed Controller Enclosure Detection

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5.0.0-green.svg)](https://opencv.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.31-purple.svg)](https://onnxruntime.ai/)
[![License: Academic](https://img.shields.io/badge/License-Academic_Evaluation-orange.svg)]()

Industrial Edge AI computer vision project for detecting the assembled enclosure of the **Rhino Motion RMCS-610 Digital Speed Controller** in real-time camera streams.

---

## 1. Project Overview & Scope

- **Target Object:** Assembled Enclosure (Lid + Base).
- **Single YOLO Detection Class:** `Class ID: 0`, `enclosure`.
- **Primary CAD Reference:** `cad/original/Rhino+Motion+RMCS-610+digital+speed+controller.stp` (AP214 STEP).
- **Secondary Mesh Reference:** `cad/original/Rhino+Motion+RMCS-610+digital+speed+controller.stl` (Binary STL).
- **Physical Envelope Dimensions:** $81.50\text{ mm (Length)} \times 73.70\text{ mm (Width)} \times 18.00\text{ mm (Height)}$.
- **Exclusion Policy:** Internal electronic components (`component` body in CAD) are internal structures and are excluded from object detection.
- **Academic Integrity:** All measurements, frame captures, and benchmarks originate from actual hardware execution. No synthetic CAD renders or fabricated data are used.

---

## 2. Six M1 Official Deliverable Folders

In accordance with official submission requirements, all six evidence dossiers reside directly at repository root:

| Deliverable Folder | Milestone Title | Key Evidence Contained | Status |
| :--- | :--- | :--- | :--- |
| [`01_camera_and_repo/`](01_camera_and_repo/) | **Camera and Repository** | Genuine `first_frame.jpg` (1280x720), `camera_specification.json`, empirical test logs | **COMPLETE** |
| [`02_opencv_pipeline/`](02_opencv_pipeline/) | **OpenCV Pipeline** | Live HUD overlays (`mode_a_pipeline.jpg`, `mode_b_pipeline.jpg`), demonstration instructions | **COMPLETE** |
| [`03_baseline_speed/`](03_baseline_speed/) | **Baseline Speed** | 186-frame `benchmark_results.csv`, `latency_fps_chart.png`, `cpu_ram_chart.png` | **COMPLETE** |
| [`04_dataset_v1/`](04_dataset_v1/) | **Dataset V1** | Dataset schema (`dataset.yaml`, `classes.txt`), annotator tool, validator report, dataset card | **PENDING DATA** |
| [`05_correct_split/`](05_correct_split/) | **Correct Split** | 70/20/10 split policy, `split_distribution.png`, cross-split leakage verification | **PENDING DATA** |
| [`06_train_and_run_detector/`](06_train_and_run_detector/) | **Train & Run Detector** | ONNX weights (19.06 ms latency), prediction overlays (`pred_first_frame.jpg`), 10-error analysis | **PENDING TRAINING** |

---

## 3. Host System Hardware & Runtime Audit

- **Operating System:** Microsoft Windows 11 Home 64-bit (Build 10.0.26300)
- **Processor (CPU):** AMD Ryzen 9 8940HX with Radeon Graphics (16 Cores, 32 Threads)
- **System Memory:** 16 GB Physical RAM (~4.1 GB Available Free)
- **Graphics Accelerator (GPU):** NVIDIA GeForce RTX 5070 Laptop GPU (12,227 MiB VRAM, Driver 617.42)
- **Vision Sensor:** Integrated HD Camera (`USB\VID_3277&PID_0010`) via OpenCV DirectShow

---

## 4. Setup & Installation

```powershell
# 1. Clone repository
git clone <YOUR_REPO_URL>
cd "Edge AI - Assignment 1"

# 2. Create isolated virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install core dependencies
pip install -r requirements.txt
```

---

## 5. Execution Commands

### Milestone 1: Camera Discovery & Frame Capture
```powershell
python camera/camera_info.py
python camera/camera_test.py
python camera/camera_capture.py --output 01_camera_and_repo/first_frame.jpg
```

### Milestone 2: Real-Time OpenCV Pipeline
```powershell
# Mode A: Camera Passthrough with Telemetry HUD
python pipeline/opencv_pipeline.py --mode A

# Mode B: Live YOLO Enclosure Detection
python pipeline/opencv_pipeline.py --mode B --model models/enclosure_detector_base.onnx
```

### Milestone 3: Baseline Latency & Hardware Profiling
```powershell
python benchmark/run_benchmark.py --duration 15 --width 1280 --height 720
```

### Milestone 4: Image Annotation & Quality Validation
```powershell
# Interactive GUI annotation tool
python dataset/annotate_dataset.py

# Automated dataset validation
python dataset/validate_dataset.py
```

### Milestone 5: 70/20/10 Split & Leakage Audit
```powershell
python dataset/split_dataset.py
python dataset/check_leakage.py
```

### Milestone 6: Model Training, Inference & Diagnostics
```powershell
# Run inference on test image
python training/inference.py --source 01_camera_and_repo/first_frame.jpg

# Train YOLO detector once dataset is populated
python training/train.py --epochs 50

# Evaluate model on test set
python training/evaluate.py

# Run failure mode error analysis
python training/error_analysis.py
```

### Automated Pytest Suite
```powershell
pytest tests/ -v
```

---

## 6. Official Submission Table & Links

The comprehensive submission table linking each deliverable to its verified evidence folder is documented in:  
📄 **[`docs/M1_assessment_submission_links.md`](docs/M1_assessment_submission_links.md)**
