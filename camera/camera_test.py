"""
Camera Functional & Stress Test Suite
Verifies camera connectivity, empirical streaming FPS, frame integrity,
and error handling.
"""

import sys
import os
import time
import json
import cv2
import numpy as np

def test_camera_connection(cam_index=0, width=1280, height=720):
    """Test connection and property negotiation."""
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(cam_index, backend)
    
    if not cap.isOpened():
        return {
            "success": False,
            "error": f"Failed to open camera index {cam_index}"
        }
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        return {
            "success": False,
            "error": "Camera opened but failed to capture a frame."
        }
        
    mean_brightness = float(np.mean(frame))
    is_valid_frame = frame.shape[0] > 0 and frame.shape[1] > 0 and len(frame.shape) == 3
    
    return {
        "success": True,
        "index": cam_index,
        "requested_resolution": [width, height],
        "actual_resolution": [actual_w, actual_h],
        "frame_shape": list(frame.shape),
        "mean_brightness": round(mean_brightness, 2),
        "valid_frame": is_valid_frame
    }

def measure_actual_fps(cam_index=0, num_frames=60, width=640, height=480):
    """Measure empirical FPS over a sustained window of real captured frames."""
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(cam_index, backend)
    
    if not cap.isOpened():
        return {"error": f"Camera index {cam_index} unavailable"}
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Warm up sensor for 5 frames
    for _ in range(5):
        cap.read()
        
    timestamps = []
    latencies_ms = []
    
    t_start = time.perf_counter()
    for _ in range(num_frames):
        t0 = time.perf_counter()
        ret, frame = cap.read()
        t1 = time.perf_counter()
        if not ret or frame is None:
            break
        latencies_ms.append((t1 - t0) * 1000.0)
        timestamps.append(t1)
        
    t_total = time.perf_counter() - t_start
    cap.release()
    
    frames_captured = len(latencies_ms)
    actual_fps = frames_captured / t_total if t_total > 0 else 0.0
    avg_latency = np.mean(latencies_ms) if latencies_ms else 0.0
    std_latency = np.std(latencies_ms) if latencies_ms else 0.0
    
    return {
        "frames_requested": num_frames,
        "frames_captured": frames_captured,
        "total_elapsed_seconds": round(t_total, 4),
        "actual_measured_fps": round(actual_fps, 2),
        "avg_frame_capture_latency_ms": round(float(avg_latency), 3),
        "std_frame_capture_latency_ms": round(float(std_latency), 3),
        "p95_latency_ms": round(float(np.percentile(latencies_ms, 95)), 3) if latencies_ms else 0.0
    }

def test_invalid_camera_handling():
    """Verify robust error handling for nonexistent devices."""
    invalid_index = 99
    cap = cv2.VideoCapture(invalid_index)
    opened = cap.isOpened()
    if opened:
        ret, frame = cap.read()
        cap.release()
    else:
        ret = False
    return {
        "invalid_index_tested": invalid_index,
        "correctly_rejected": not opened or not ret,
        "handled_gracefully": True
    }

if __name__ == "__main__":
    print("=" * 60)
    print("EXECUTING CAMERA CAPTURE VERIFICATION SUITE")
    print("=" * 60)
    
    conn_result = test_camera_connection()
    print("1. Connection Test Result:")
    print(json.dumps(conn_result, indent=2))
    
    print("\n2. Empirical FPS & Latency Measurement (60 Frames):")
    fps_result = measure_actual_fps(num_frames=60)
    print(json.dumps(fps_result, indent=2))
    
    print("\n3. Error & Disconnection Handling Test:")
    error_result = test_invalid_camera_handling()
    print(json.dumps(error_result, indent=2))
    
    # Save test logs to 01_camera_and_repo
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_camera_and_repo"))
    os.makedirs(out_dir, exist_ok=True)
    report = {
        "connection_test": conn_result,
        "fps_measurement": fps_result,
        "error_handling_test": error_result,
        "status": "PASSED" if conn_result.get("success") else "FAILED"
    }
    with open(os.path.join(out_dir, "camera_test_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[+] Full test report saved to: {os.path.join(out_dir, 'camera_test_report.json')}")

