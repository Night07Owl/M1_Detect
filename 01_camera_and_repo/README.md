# Deliverable 1: Camera and Repository Evidence Dossier

**Milestone:** M1 (DETECT)  
**Deliverable ID:** D1 – Camera and Repository  
**Target:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Repository Branch:** `main`  
**Date of Acquisition:** November 10, 2026

---

## 1. Verified Evidence Files in this Folder

| File Name | Description | Verification Method |
| :--- | :--- | :--- |
| `first_frame.jpg` | First genuine physical camera frame (1280 x 720) | Captured via `camera/camera_capture.py` directly from USB sensor |
| `camera_specification.json` | JSON audit of connected cameras and supported properties | Discovered via `camera/camera_info.py` and WMI/CIM query |
| `camera_specification.md` | Detailed sensor datasheet & DirectShow configuration | Consolidated technical analysis |
| `camera_test_report.json` | Empirical 60-frame benchmark, latency, and error handling | Executed via `camera/camera_test.py` |
| `hardware_specification.md` | Full system audit (AMD Ryzen 9, RTX 5070, 16GB RAM) | Discovered via WMI, CIM, and NVIDIA-SMI |
| `repository_information.md` | Git structure, commit logs, branches, and tree verification | Git CLI verification |
| `setup_instructions.md` | Step-by-step reproduction guide for examiner | Standardized workflow |

---

## 2. Key Sensor Findings

- **Device Name:** Integrated Camera (Manufacturer: Sonix)
- **Hardware PnP ID:** `USB\VID_3277&PID_0010&MI_00\7&DF5034D&0&0000`
- **Stream Backend:** OpenCV DirectShow (`cv2.CAP_DSHOW`)
- **Operational Resolution:** $1280 \times 720$ pixels (HD)
- **Measured Capture Latency:** $50.39\text{ ms}$ (empirical frame rate: $19.84\text{ FPS}$)
- **Frame Validation:** Valid 3-channel BGR matrix, non-zero pixel density.
