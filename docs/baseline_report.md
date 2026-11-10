# Edge AI Baseline Performance & Hardware Report

**Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Evaluation Date:** November 10, 2026  
**Benchmarking Engine:** `benchmark/run_benchmark.py`  
**Execution Environment:** Windows 11 Home 64-bit, Python 3.11.9, OpenCV 5.0.0.93  

---

## 1. Executive Summary

An empirical baseline performance profile was executed directly on the host edge workstation. The benchmark measured sustained frame rates, decomposed camera acquisition from algorithmic compute latency, and logged CPU, GPU, memory, and thermal telemetry across 186 continuously acquired frames.

| Metric | Measured Baseline Value | Target / Assessment Expectation | Status |
| :--- | :--- | :--- | :--- |
| **Operational Frame Rate** | **16.65 FPS** (Median: 20.76 FPS, P95: 21.28 FPS) | Real-time threshold ($\ge 15\text{ FPS}$) | MET |
| **Mean Camera Capture Latency** | **47.92 ms** | Hardware I/O DirectShow constraint | AUDITED |
| **Mean Baseline Compute Latency** | **1.84 ms** | Preprocessing (RGB $\to$ Gray $\to$ Blur $\to$ Canny) | MET |
| **Mean Total Pipeline Latency** | **49.75 ms** (P95: 64.36 ms) | Real-time interactive latency ($< 100\text{ ms}$) | MET |
| **Host System CPU Load** | **5.82%** | AMD Ryzen 9 8940HX (16 Cores, 32 Threads) | MET |
| **Process Resident Memory (RSS)** | **136.22 MB** | Embedded workstation RAM envelope | MET |
| **GPU Core Temperature** | **47.0 °C** | NVIDIA GeForce RTX 5070 Laptop GPU | MET |
| **GPU Utilization (Baseline)** | **0.0%** (Idle during non-DNN baseline) | Baseline before neural weight offload | AUDITED |

---

## 2. Experimental Setup & Hardware Configuration

- **Central Processing Unit (CPU):** AMD Ryzen 9 8940HX with Radeon Graphics (16 Physical Cores, 32 Threads)
- **Dedicated Graphics (GPU):** NVIDIA GeForce RTX 5070 Laptop GPU (12,227 MiB VRAM, Driver 617.42)
- **Sensor:** Integrated HD Camera (`USB\VID_3277&PID_0010`)
- **Camera Resolution:** $1280 \times 720$ (16:9 High Definition)
- **OpenCV Backend:** DirectShow (`cv2.CAP_DSHOW`)
- **Sample Window:** 186 frames evaluated over 11.17 seconds
- **Sampling Interval:** Instantaneous frame delta $\Delta t$ with 5-frame subsystem hardware polling.

---

## 3. Latency Decomposition Analysis

The latency measurements rigorously differentiate between **hardware acquisition delay** and **algorithmic processing delay**:

$$T_{\text{total}} = T_{\text{capture}} + T_{\text{processing}}$$

- **Camera Capture Latency ($T_{\text{capture}}$):**
  - Mean: $47.92\text{ ms}$
  - Analysis: The camera sensor operates at a nominal ~20–30 Hz exposure cycle under current ambient indoor luminescence. The hardware exposure and USB UVC bus transfer accounts for $96.3\%$ of the total pipeline turnaround time in the unweighted baseline.
- **Image Processing Latency ($T_{\text{processing}}$):**
  - Mean: $1.84\text{ ms}$
  - Analysis: Edge filtering (grayscale transformation, $5 \times 5$ Gaussian kernel smoothing, and Canny gradient edge extraction) requires only $1.84\text{ ms}$ on the AMD Ryzen 9 workstation, demonstrating ample compute headroom for deep neural network inference.

---

## 4. Visual Evidence Artifacts

1. **Latency & Frame Rate Time Series:** `03_baseline_speed/latency_fps_chart.png`  
   Displays total latency vs. capture latency alongside the instantaneous FPS trajectory over the benchmarking duration.
2. **Resource Consumption Curve:** `03_baseline_speed/cpu_ram_chart.png`  
   Demonstrates steady process memory allocation ($136.2\text{ MB}$) and process CPU utilization without memory leakage or thrashing.
3. **Raw Measurement Log:** `03_baseline_speed/benchmark_results.csv`  
   186 individual per-frame timestamped records containing instantaneous latency, FPS, CPU, RAM, and GPU telemetry.

---

## 5. Command to Reproduce Measurements on Host Device

To re-run the benchmark on the host machine and collect updated empirical telemetry:

```powershell
python benchmark/run_benchmark.py --duration 15 --width 1280 --height 720
```
