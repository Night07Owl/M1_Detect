# M1 Assessment Submission Links

**Student Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Module:** Edge AI & Real-Time Computer Vision  
**Milestone:** Milestone 1 (M1 – DETECT)  
**Verified GitHub Repository:** [https://github.com/Night07Owl/M1_Detect](https://github.com/Night07Owl/M1_Detect)  
**Verification Date:** November 10, 2026  

---

## 1. Six Assessment Submission Links Table

| # | Assessment Requirement | GitHub Link | Evidence Contents | Milestone Status |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Camera and repo** | [https://github.com/Night07Owl/M1_Detect/tree/main/01_camera_and_repo](https://github.com/Night07Owl/M1_Detect/tree/main/01_camera_and_repo) | Genuine `first_frame.jpg` (1280x720), `camera_specification.json`, `camera_test_report.json`, hardware audit | **COMPLETE** |
| **2** | **OpenCV pipeline** | [https://github.com/Night07Owl/M1_Detect/tree/main/02_opencv_pipeline](https://github.com/Night07Owl/M1_Detect/tree/main/02_opencv_pipeline) | Live HUD overlays (`mode_a_pipeline.jpg`, `mode_b_pipeline.jpg`), demonstration guide, telemetry specs | **COMPLETE** |
| **3** | **Baseline speed** | [https://github.com/Night07Owl/M1_Detect/tree/main/03_baseline_speed](https://github.com/Night07Owl/M1_Detect/tree/main/03_baseline_speed) | 186-frame empirical `benchmark_results.csv`, `latency_fps_chart.png`, `cpu_ram_chart.png`, summary JSON | **COMPLETE** |
| **4** | **Dataset V1** | [https://github.com/Night07Owl/M1_Detect/tree/main/04_dataset_v1](https://github.com/Night07Owl/M1_Detect/tree/main/04_dataset_v1) | Dataset schema (`dataset.yaml`, `classes.txt`), annotator tool, validator report, formal dataset card | **PENDING DATA**<br>*(Tooling COMPLETE)* |
| **5** | **Correct split** | [https://github.com/Night07Owl/M1_Detect/tree/main/05_correct_split](https://github.com/Night07Owl/M1_Detect/tree/main/05_correct_split) | 70/20/10 split policy, `split_distribution.png`, leakage audit (`leakage_verification.txt`, report JSON) | **PENDING DATA**<br>*(Tooling COMPLETE)* |
| **6** | **Train and run detector** | [https://github.com/Night07Owl/M1_Detect/tree/main/06_train_and_run_detector](https://github.com/Night07Owl/M1_Detect/tree/main/06_train_and_run_detector) | ONNX edge weights (19.06 ms latency), prediction overlays (`pred_first_frame.jpg`), 10-error analysis | **PENDING TRAINING**<br>*(Inference COMPLETE)* |

---

## 2. Assessment Evidence Directory Mapping

All six evidence dossiers reside directly at the root of the repository as required:

- **Folder 1:** [`01_camera_and_repo/`](https://github.com/Night07Owl/M1_Detect/tree/main/01_camera_and_repo)
- **Folder 2:** [`02_opencv_pipeline/`](https://github.com/Night07Owl/M1_Detect/tree/main/02_opencv_pipeline)
- **Folder 3:** [`03_baseline_speed/`](https://github.com/Night07Owl/M1_Detect/tree/main/03_baseline_speed)
- **Folder 4:** [`04_dataset_v1/`](https://github.com/Night07Owl/M1_Detect/tree/main/04_dataset_v1)
- **Folder 5:** [`05_correct_split/`](https://github.com/Night07Owl/M1_Detect/tree/main/05_correct_split)
- **Folder 6:** [`06_train_and_run_detector/`](https://github.com/Night07Owl/M1_Detect/tree/main/06_train_and_run_detector)
