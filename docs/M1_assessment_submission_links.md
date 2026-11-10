# M1 Assessment Submission Links

**Student Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Module:** Edge AI & Real-Time Computer Vision  
**Milestone:** Milestone 1 (M1 – DETECT)  
**Verification Date:** November 10, 2026  

---

## 1. Assessment Submission Table

> [!IMPORTANT]
> **Anti-Fabrication Rule:** In accordance with the prompt instructions ("Only populate GitHub links after verifying the actual repository URL and the existence of each folder. Do not generate fake links"), no remote was configured on this local machine at time of audit (`git remote -v` returned empty).  
> Once you link your remote via `git remote add origin <YOUR_GITHUB_URL>` and push with your approval, each folder link below resolves to `<YOUR_GITHUB_URL>/tree/main/<FOLDER_NAME>`. The verified folder paths and audited contents are recorded below:

| # | Assessment Requirement | Folder Relative Path | Verified Evidence Contents | Milestone Status | Submission URL Template |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Camera and Repo** | `01_camera_and_repo/` | Genuine `first_frame.jpg` (1280x720), `camera_specification.json`, `camera_test_report.json`, hardware audit | **COMPLETE** | `[REPO_URL]/tree/main/01_camera_and_repo` |
| **2** | **OpenCV Pipeline** | `02_opencv_pipeline/` | `mode_a_pipeline.jpg`, `mode_b_pipeline.jpg`, live HUD telemetry overlays, demonstration guide | **COMPLETE** | `[REPO_URL]/tree/main/02_opencv_pipeline` |
| **3** | **Baseline Speed** | `03_baseline_speed/` | 186-frame empirical `benchmark_results.csv`, `latency_fps_chart.png`, `cpu_ram_chart.png`, summary JSON | **COMPLETE** | `[REPO_URL]/tree/main/03_baseline_speed` |
| **4** | **Dataset V1** | `04_dataset_v1/` | Dataset schema (`dataset.yaml`, `classes.txt`), annotator tool, validator report, formal dataset card | **PENDING DATA** (Infrastructure COMPLETE) | `[REPO_URL]/tree/main/04_dataset_v1` |
| **5** | **Correct Split** | `05_correct_split/` | 70/20/10 split policy, `split_distribution.png`, leakage audit (`leakage_verification.txt`, report JSON) | **PENDING DATA** (Infrastructure COMPLETE) | `[REPO_URL]/tree/main/05_correct_split` |
| **6** | **Train & Run Detector** | `06_train_and_run_detector/` | ONNX edge weights (19.06 ms latency), prediction overlays (`pred_first_frame.jpg`), 10-error analysis framework | **PENDING TRAINING** (Inference COMPLETE) | `[REPO_URL]/tree/main/06_train_and_run_detector` |

---

## 2. Steps to Connect and Generate Exact GitHub URLs

1. Add your personal GitHub repository remote:
   ```powershell
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git
   ```
2. Push the verified `main` branch:
   ```powershell
   git push -u origin main
   ```
3. Replace `[REPO_URL]` in the table with your verified repository URL (e.g., `https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>`).

