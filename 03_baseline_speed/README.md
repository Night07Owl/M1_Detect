# Deliverable 3: Baseline Speed & Resource Benchmarking Dossier

**Milestone:** M1 (DETECT)  
**Deliverable ID:** D3 – Baseline Speed  
**Target Object:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure  
**Benchmark Script:** `benchmark/run_benchmark.py`  
**Execution Date:** November 10, 2026

---

## 1. Verified Evidence Files in this Folder

| File Name | Description | Verification Method |
| :--- | :--- | :--- |
| `benchmark_results.csv` | 186 per-frame empirical measurement rows (FPS, latencies, CPU %, RAM MB, GPU %, Temp °C) | Generated directly by `benchmark/run_benchmark.py` |
| `benchmark_summary.json` | Statistical summary (mean, median, p95 FPS, latencies, resource aggregates) | Exported JSON summary |
| `latency_fps_chart.png` | High-resolution plot of pipeline latency breakdown and streaming FPS | Matplotlib visualization from empirical CSV |
| `cpu_ram_chart.png` | Process CPU utilization and resident memory consumption curve | Matplotlib visualization from empirical CSV |

---

## 2. Empirical Benchmark Summary (186 Frames @ 1280x720)

- **Average Operational FPS:** **16.65 FPS** (P50: 20.76 FPS, P95: 21.28 FPS)
- **Average Camera Capture Latency:** **47.92 ms**
- **Average Baseline Compute Latency:** **1.84 ms**
- **Average Total Pipeline Latency:** **49.75 ms** (P95: 64.36 ms)
- **Process Memory Footprint:** **136.22 MB** RSS
- **System CPU Load:** **5.82%**
- **GPU Core Temperature:** **47.0 °C** (NVIDIA RTX 5070 Laptop GPU)

---

## 3. Exact Reproduction Command
```powershell
python benchmark/run_benchmark.py --duration 15 --width 1280 --height 720
```

