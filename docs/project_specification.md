# Project Specification: IDRP M1 (DETECT)

**Target Object:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure  
**Module:** Edge AI & Real-Time Computer Vision  
**Phase:** Milestone 1 (M1 – Detect)  
**Author:** Senior Edge AI / Computer Vision Engineer  
**Date:** November 10, 2026

---

## 1. Project Background & Objective

The objective of Milestone 1 (M1) is to establish a robust, verifiable Edge AI vision pipeline capable of detecting the physical enclosure of a **Rhino Motion RMCS-610 Digital Speed Controller** in real-time camera streams.

The RMCS-610 is an industrial closed-loop digital speed controller housed within a two-part protective housing (lid and base). In operational edge deployment scenarios (e.g. quality assurance, robotic pick-and-place, automated optical inspection), the vision system must detect the assembled enclosure under varying angles, distances, and lighting conditions.

---

## 2. Detection Scope & Bounding Box Rules

- **Detection Class:** Single-class object detection.
  - **Class ID:** `0`
  - **Class Name:** `enclosure`
- **Definition:** The assembled enclosure (consisting of the upper lid and the lower base mounted together) represents **ONE single physical object**.
- **Bounding Box Annotation:** Exactly one tight bounding box encompassing the visible external housing.
- **Internal Components:** The internal printed circuit board (PCB), terminals, and electronic components (`component` in CAD) must be excluded from independent detection.
- **Authenticity Mandate:** Only real camera photographs of the physical enclosure may be utilized in the training, validation, and testing datasets. No synthetic CAD renders or fabricated labels are permitted.

---

## 3. Official Assessment Deliverables (M1)

The assignment requires six specific deliverables, each tied to genuine physical evidence stored in numbered root folders:

| Milestone Link | Folder Path | Key Deliverable | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **Deliverable 1** | `01_camera_and_repo/` | Camera and Repository | Real first frame, camera specs, hardware info, verified setup guide |
| **Deliverable 2** | `02_opencv_pipeline/` | OpenCV Pipeline | Real-time OpenCV application with overlays, FPS/latency HUD, Modes A & B |
| **Deliverable 3** | `03_baseline_speed/` | Baseline Speed | Empirical latency/FPS benchmarks, CPU/GPU usage, temperature, CSV & charts |
| **Deliverable 4** | `04_dataset_v1/` | Dataset V1 | Real photos, normalized YOLO labels, visual annotations, dataset card |
| **Deliverable 5** | `05_correct_split/` | Correct Split | Strict 70/20/10 split, zero data leakage verification, distribution charts |
| **Deliverable 6** | `06_train_and_run_detector/` | Train & Run Detector | Trained YOLO model, evaluation metrics (mAP, P, R, CM), error analysis (10 errors) |

---

## 4. Repository Layout & Evidence Standards

All evidence folders reside directly in the root directory:

```text
PROJECT_ROOT/
├── 01_camera_and_repo/           # Milestone 1: Camera capture evidence & hardware audits
├── 02_opencv_pipeline/          # Milestone 2: OpenCV HUD & pipeline overlay evidence
├── 03_baseline_speed/           # Milestone 3: Real benchmark logs, CSVs, and latency curves
├── 04_dataset_v1/               # Milestone 4: Annotated sample crops, YAML, dataset card
├── 05_correct_split/            # Milestone 5: Split report, leakage check logs, charts
├── 06_train_and_run_detector/   # Milestone 6: Model metrics, PR curves, 10 error analyses
├── cad/
│   ├── original/                # Original STEP, STL, and F3D files (unmodified)
│   └── analysis/                # Dimensional analysis JSON and geometric extractions
├── camera/                      # Camera acquisition modules (discovery, test, capture)
├── pipeline/                    # Real-time computer vision pipeline (Modes A & B)
├── benchmark/                   # System profiler & latency benchmarking engine
├── dataset/                     # Local annotation tools, splitters, leakage validators
├── training/                    # YOLO training, evaluation, validation, and ONNX export
├── models/                      # Trained model weights and exported ONNX models
├── results/                     # Raw CSVs, confusion matrices, prediction overlays
├── docs/                        # Complete technical documentation suite
└── tests/                       # Automated pytest test suites
```

---

## 5. Academic Integrity & Anti-Fabrication Rule

In compliance with the assignment instructions:
1. Every measurement, frame, and benchmark reported must originate from actual execution.
2. If physical hardware or user-collected dataset photographs are pending, the status is explicitly documented as `PENDING HARDWARE` or `PENDING DATA`.
3. The requirement for "Two developed 3D models" is documented as requiring lecturer clarification, rather than artificially separating CAD components.

