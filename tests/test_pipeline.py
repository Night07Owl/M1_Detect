"""
Test Suite: OpenCV Pipeline Components & Telemetry HUD
"""

import numpy as np
import cv2
from pipeline.performance_monitor import PerformanceMonitor
from pipeline.visualization import draw_hud, draw_detections
from pipeline.detector import EnclosureDetector

def test_performance_monitor():
    pm = PerformanceMonitor(window_size=10)
    pm.record_capture_latency(45.0)
    pm.record_inference_latency(15.0)
    pm.record_total_latency(60.0)
    pm.tick_frame()
    
    assert pm.get_avg_capture_latency() == 45.0
    assert pm.get_avg_inference_latency() == 15.0
    assert pm.get_avg_total_latency() == 60.0
    summary = pm.get_summary()
    assert summary["total_frames"] == 1

def test_visualization_hud():
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    out = draw_hud(dummy, mode="A", fps=30.0, latency_ms=33.3, enclosure_count=0)
    assert out.shape == (480, 640, 3)
    # Check that pixels were drawn (not all zero anymore)
    assert np.count_nonzero(out) > 0

def test_visualization_detections():
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    dets = [{
        "box": [50, 50, 200, 200],
        "class_id": 0,
        "class_name": "enclosure",
        "confidence": 0.95
    }]
    out = draw_detections(dummy, dets)
    assert np.count_nonzero(out) > 0

def test_detector_inference():
    det = EnclosureDetector(model_path="models/enclosure_detector_base.onnx", conf_thres=0.35)
    assert det.is_loaded() is True
    dummy = np.zeros((720, 1280, 3), dtype=np.uint8)
    res = det.detect(dummy)
    assert isinstance(res, list)
