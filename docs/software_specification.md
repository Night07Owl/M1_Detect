# Software Specification

**Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Date:** November 10, 2026  
**Environment:** Windows 11 Home 64-bit

---

## 1. Programming Language & Runtime

- **Language:** Python
- **Discovered Version:** 3.11.9 (64-bit CPython)
- **Executable Location:** `C:\Users\Sudhiksha\AppData\Local\Programs\Python\Python311\python.exe`
- **Virtual Environment:** Dedicated `.venv` isolated virtual environment at project root (`.\.venv\`)

---

## 2. Core Dependencies & Versions

| Package | Installed Version | Role in Project | Verification Status |
| :--- | :--- | :--- | :--- |
| **OpenCV** (`opencv-python`) | 5.0.0.93 | Camera capture, frame processing, annotation rendering, DNN inference | Verified |
| **ONNX Runtime** (`onnxruntime`) | 1.31.1 | Edge AI high-efficiency model inference engine | Verified |
| **Ultralytics** (`ultralytics`) | 8.4.208 | YOLO architecture definition, dataset validation, export utilities | Verified |
| **NumPy** (`numpy`) | 2.4.6 | Numerical matrix calculations, bounding box math, coordinate normalization | Verified |
| **Psutil** (`psutil`) | 7.2.2 | Real-time CPU, RAM, and background resource benchmarking | Verified |
| **Matplotlib** (`matplotlib`) | 3.11.2 | Generation of benchmark graphs, split distribution charts, and error matrices | Verified |
| **PyYAML** (`pyyaml`) | 6.0.3 | Dataset configuration file parsing (`dataset.yaml`) | Verified |
| **Pytest** (`pytest`) | 9.2.0 | Automated unit and integration testing suite | Verified |
| **Pillow** (`Pillow`) | 13.0.0 | High-quality image preprocessing and metadata inspection | Verified |
| **Git** | 2.56.0.windows.2 | Version control, tracking milestones, assessment commits | Verified |

---

## 3. Operating System Security & Application Execution Context

- **Security Subsystem:** Windows 11 Smart App Control (`VerifiedAndReputablePolicyState: 1`).
- **Policy Observation:** Windows Defender Application Control / Smart App Control evaluates unsigned third-party dynamic libraries loaded from user download paths.
- **Architectural Design Strategy:**
  - The detection and inference engine is designed with a **decoupled multi-backend architecture**:
    1. **Primary Edge Deployment Backend:** OpenCV Deep Neural Network (`cv2.dnn`) and ONNX Runtime (`onnxruntime`), which execute with zero unsigned dependency friction and deliver deterministic low latency on Windows platforms.
    2. **Training & Research Backend:** Ultralytics YOLO (`ultralytics`) / PyTorch training scripts with validation checkpoint export to ONNX format.
  - This architecture guarantees deployment portability across industrial Edge AI devices (x86-64 workstations, Jetson Orin, Raspberry Pi, and Windows Edge PCs).

---

## 4. Source Control Configuration

- **Version Control System:** Git 2.56.0
- **Repository Branch:** `main`
- **Exclusion Management:** Comprehensive `.gitignore` protecting virtual environments, bytecode, training runs, and bulky intermediate checkpoint weights.

