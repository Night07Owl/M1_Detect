"""
Real-Time Performance Monitor
Tracks frame capture latency, inference latency, total latency, and rolling FPS.
"""

import time
from collections import deque
import numpy as np

class PerformanceMonitor:
    def __init__(self, window_size=30):
        self.window_size = window_size
        self.frame_times = deque(maxlen=window_size)
        self.capture_latencies = deque(maxlen=window_size)
        self.inference_latencies = deque(maxlen=window_size)
        self.total_latencies = deque(maxlen=window_size)
        
        self.last_frame_timestamp = None
        self.total_frames_processed = 0
        self.start_time = time.perf_counter()

    def record_capture_latency(self, duration_ms):
        self.capture_latencies.append(duration_ms)

    def record_inference_latency(self, duration_ms):
        self.inference_latencies.append(duration_ms)

    def record_total_latency(self, duration_ms):
        self.total_latencies.append(duration_ms)

    def tick_frame(self):
        now = time.perf_counter()
        if self.last_frame_timestamp is not None:
            dt = now - self.last_frame_timestamp
            if dt > 0:
                self.frame_times.append(dt)
        self.last_frame_timestamp = now
        self.total_frames_processed += 1

    def get_fps(self):
        if not self.frame_times:
            return 0.0
        return len(self.frame_times) / sum(self.frame_times)

    def get_avg_capture_latency(self):
        return np.mean(self.capture_latencies) if self.capture_latencies else 0.0

    def get_avg_inference_latency(self):
        return np.mean(self.inference_latencies) if self.inference_latencies else 0.0

    def get_avg_total_latency(self):
        return np.mean(self.total_latencies) if self.total_latencies else 0.0

    def get_summary(self):
        elapsed = time.perf_counter() - self.start_time
        return {
            "total_frames": self.total_frames_processed,
            "elapsed_seconds": round(elapsed, 3),
            "fps": round(self.get_fps(), 2),
            "avg_capture_latency_ms": round(float(self.get_avg_capture_latency()), 2),
            "avg_inference_latency_ms": round(float(self.get_avg_inference_latency()), 2),
            "avg_total_latency_ms": round(float(self.get_avg_total_latency()), 2),
            "p95_total_latency_ms": round(float(np.percentile(self.total_latencies, 95)), 2) if self.total_latencies else 0.0
        }
