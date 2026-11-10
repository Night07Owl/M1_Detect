"""
Edge AI Baseline Speed & Resource Benchmarking System
Executes sustained performance profiling of the camera pipeline and edge vision processing.
Separates camera capture time from frame processing time.
Outputs CSV logs, summary JSON, and performance visualization charts.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import argparse
import csv
import json
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from benchmark.system_monitor import SystemMonitor

def run_benchmark(duration_seconds=15, cam_index=0, width=1280, height=720,
                  output_dir="results/benchmarks", evidence_dir="03_baseline_speed"):
    """
    Run empirical system performance benchmark.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(evidence_dir, exist_ok=True)
    
    print("=" * 65)
    print("STARTING BASELINE SPEED & HARDWARE PROFILING BENCHMARK")
    print(f"Target Duration: {duration_seconds} seconds")
    print(f"Camera Requested: index {cam_index} ({width}x{height})")
    print("=" * 65)
    
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(cam_index, backend)
    
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {cam_index} for benchmarking.")
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Warm up camera for 5 frames
    for _ in range(5):
        cap.read()
        
    monitor = SystemMonitor()
    records = []
    
    start_time = time.perf_counter()
    prev_frame_time = start_time
    frame_count = 0
    
    print("[+] Collecting live benchmark measurements...")
    while True:
        now = time.perf_counter()
        elapsed_total = now - start_time
        if elapsed_total >= duration_seconds:
            break
            
        # 1. Camera Capture Measurement
        t_cap_start = time.perf_counter()
        ret, frame = cap.read()
        t_cap_end = time.perf_counter()
        
        if not ret or frame is None:
            break
            
        capture_latency_ms = (t_cap_end - t_cap_start) * 1000.0
        
        # 2. Standard Baseline Processing Simulation (Color conversion, blurring, thresholding)
        t_proc_start = time.perf_counter()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        t_proc_end = time.perf_counter()
        
        processing_latency_ms = (t_proc_end - t_proc_start) * 1000.0
        total_latency_ms = capture_latency_ms + processing_latency_ms
        
        # Calculate instantaneous FPS
        dt = t_proc_end - prev_frame_time
        inst_fps = 1.0 / dt if dt > 0 else 0.0
        prev_frame_time = t_proc_end
        frame_count += 1
        
        # Capture hardware snapshot every 5 frames to avoid profiling overhead
        if frame_count % 5 == 0 or frame_count == 1:
            sys_snap = monitor.get_snapshot()
        
        record = {
            "frame_id": frame_count,
            "timestamp_sec": round(elapsed_total, 4),
            "capture_latency_ms": round(capture_latency_ms, 3),
            "processing_latency_ms": round(processing_latency_ms, 3),
            "total_latency_ms": round(total_latency_ms, 3),
            "instantaneous_fps": round(inst_fps, 2),
            "proc_cpu_percent": sys_snap["process_cpu_percent"],
            "sys_cpu_percent": sys_snap["system_cpu_percent"],
            "proc_ram_mb": sys_snap["process_ram_mb"],
            "sys_ram_percent": sys_snap["system_ram_percent"],
            "gpu_util_percent": sys_snap["gpu_utilization_percent"],
            "gpu_temp_c": sys_snap["gpu_temperature_c"],
            "gpu_mem_used_mb": sys_snap["gpu_memory_used_mb"]
        }
        records.append(record)
        
    cap.release()
    monitor.close()
    
    total_duration = time.perf_counter() - start_time
    avg_fps = frame_count / total_duration if total_duration > 0 else 0.0
    
    # Compute Aggregates
    cap_latencies = [r["capture_latency_ms"] for r in records]
    proc_latencies = [r["processing_latency_ms"] for r in records]
    tot_latencies = [r["total_latency_ms"] for r in records]
    fps_vals = [r["instantaneous_fps"] for r in records[1:]]  # Exclude frame 1 warmup
    proc_cpus = [r["proc_cpu_percent"] for r in records]
    sys_cpus = [r["sys_cpu_percent"] for r in records]
    proc_rams = [r["proc_ram_mb"] for r in records]
    
    gpu_utils = [r["gpu_util_percent"] for r in records if isinstance(r["gpu_util_percent"], (int, float))]
    gpu_temps = [r["gpu_temp_c"] for r in records if isinstance(r["gpu_temp_c"], (int, float))]
    
    summary = {
        "metadata": {
            "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "os": sys.platform,
            "python_version": sys.version.split()[0],
            "opencv_version": cv2.__version__,
            "camera_resolution": [actual_w, actual_h],
            "benchmark_duration_seconds": round(total_duration, 2),
            "total_frames_evaluated": frame_count
        },
        "performance_metrics": {
            "average_fps": round(avg_fps, 2),
            "p50_fps": round(float(np.median(fps_vals)), 2) if fps_vals else 0.0,
            "p95_fps": round(float(np.percentile(fps_vals, 95)), 2) if fps_vals else 0.0,
            "avg_capture_latency_ms": round(float(np.mean(cap_latencies)), 2),
            "avg_processing_latency_ms": round(float(np.mean(proc_latencies)), 2),
            "avg_total_latency_ms": round(float(np.mean(tot_latencies)), 2),
            "p95_total_latency_ms": round(float(np.percentile(tot_latencies, 95)), 2)
        },
        "system_utilization": {
            "avg_process_cpu_percent": round(float(np.mean(proc_cpus)), 2),
            "avg_system_cpu_percent": round(float(np.mean(sys_cpus)), 2),
            "avg_process_ram_mb": round(float(np.mean(proc_rams)), 2),
            "avg_gpu_utilization_percent": round(float(np.mean(gpu_utils)), 2) if gpu_utils else "Unavailable",
            "avg_gpu_temp_c": round(float(np.mean(gpu_temps)), 2) if gpu_temps else "Unavailable"
        }
    }
    
    # 1. Write CSV Log
    csv_paths = [
        os.path.join(output_dir, "benchmark_results.csv"),
        os.path.join(evidence_dir, "benchmark_results.csv")
    ]
    for p in csv_paths:
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
            
    # 2. Write JSON Summary
    summary_paths = [
        os.path.join(output_dir, "benchmark_summary.json"),
        os.path.join(evidence_dir, "benchmark_summary.json")
    ]
    for p in summary_paths:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
            
    # 3. Generate Charts
    _generate_charts(records, output_dir, evidence_dir)
    
    print("\n--- BENCHMARK COMPLETE ---")
    print(json.dumps(summary, indent=2))
    return summary

def _generate_charts(records, output_dir, evidence_dir):
    """Generate high-resolution PNG charts for latency, FPS, and resource utilization."""
    timestamps = [r["timestamp_sec"] for r in records]
    cap_lat = [r["capture_latency_ms"] for r in records]
    proc_lat = [r["processing_latency_ms"] for r in records]
    tot_lat = [r["total_latency_ms"] for r in records]
    fps = [r["instantaneous_fps"] for r in records]
    proc_cpu = [r["proc_cpu_percent"] for r in records]
    proc_ram = [r["proc_ram_mb"] for r in records]
    
    # Chart 1: Latency & Frame Rate Over Time
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(timestamps, tot_lat, label="Total Latency (ms)", color="#d9534f", linewidth=2)
    ax1.plot(timestamps, cap_lat, label="Camera Capture Latency (ms)", color="#f0ad4e", linestyle="--")
    ax1.plot(timestamps, proc_lat, label="OpenCV Processing Latency (ms)", color="#5cb85c", linestyle=":")
    ax1.set_ylabel("Latency (ms)")
    ax1.set_title("Pipeline Latency Breakdown (Empirical Measurement)", fontsize=13, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right")
    
    ax2.plot(timestamps, fps, label="Instantaneous FPS", color="#0275d8", linewidth=2)
    ax2.axhline(y=np.mean(fps[1:]), color="#025aa5", linestyle="--", label=f"Mean FPS ({np.mean(fps[1:]):.1f})")
    ax2.set_xlabel("Elapsed Time (seconds)")
    ax2.set_ylabel("Frames Per Second (FPS)")
    ax2.set_title("Streaming Frame Rate Stability", fontsize=13, fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right")
    
    plt.tight_layout()
    chart1_out = os.path.join(output_dir, "latency_fps_chart.png")
    fig.savefig(chart1_out, dpi=300)
    fig.savefig(os.path.join(evidence_dir, "latency_fps_chart.png"), dpi=300)
    plt.close(fig)
    
    # Chart 2: System Resource Consumption (CPU & RAM)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(timestamps, proc_cpu, label="Process CPU %", color="#6f42c1", linewidth=2)
    ax1.set_ylabel("CPU Utilization (%)")
    ax1.set_title("Process CPU Utilization Over Time", fontsize=13, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right")
    
    ax2.plot(timestamps, proc_ram, label="Process Memory (MB RSS)", color="#20c997", linewidth=2)
    ax2.set_xlabel("Elapsed Time (seconds)")
    ax2.set_ylabel("Memory (MB)")
    ax2.set_title("Process Resident RAM Consumption", fontsize=13, fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right")
    
    plt.tight_layout()
    chart2_out = os.path.join(output_dir, "cpu_ram_chart.png")
    fig.savefig(chart2_out, dpi=300)
    fig.savefig(os.path.join(evidence_dir, "cpu_ram_chart.png"), dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Edge AI Baseline Benchmark")
    parser.add_argument("--duration", type=int, default=15, help="Benchmark duration in seconds")
    parser.add_argument("--cam", type=int, default=0, help="Camera device index")
    parser.add_argument("--width", type=int, default=1280, help="Capture width")
    parser.add_argument("--height", type=int, default=720, help="Capture height")
    
    args = parser.parse_args()
    run_benchmark(
        duration_seconds=args.duration,
        cam_index=args.cam,
        width=args.width,
        height=args.height
    )
