"""
Camera Discovery and Hardware Information Tool
Queries connected vision sensors via OpenCV and Windows Management Instrumentation (WMI).
"""

import sys
import os
import json
import subprocess
import cv2

def get_wmi_camera_info():
    """Query Windows PNP camera hardware information via PowerShell/CIM."""
    if sys.platform != "win32":
        return []
    
    cmd = [
        "powershell", "-NoProfile", "-Command",
        "Get-CimInstance Win32_PnPEntity | "
        "Where-Object { $_.PNPClass -eq 'Camera' -or $_.PNPClass -eq 'Image' } | "
        "Select-Object Name, DeviceID, Manufacturer, Status | ConvertTo-Json"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout)
            if isinstance(data, dict):
                return [data]
            elif isinstance(data, list):
                return data
    except Exception as e:
        return [{"error": str(e)}]
    return []

def probe_opencv_cameras(max_index=4):
    """Probe OpenCV camera indices and retrieve hardware resolution/backend capabilities."""
    cameras = []
    
    # Try DirectShow first on Windows, fallback to default
    backends = [
        ("DirectShow", cv2.CAP_DSHOW) if sys.platform == "win32" else ("V4L2", cv2.CAP_V4L2),
        ("Default", cv2.CAP_ANY)
    ]
    
    for idx in range(max_index):
        for b_name, b_api in backends:
            cap = cv2.VideoCapture(idx, b_api)
            if cap.isOpened():
                # Read test frame to verify actual image streaming
                ret, frame = cap.read()
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
                fourcc_str = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])
                
                # Test higher resolution capability
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                ret_hd, frame_hd = cap.read()
                hd_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                hd_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                cap.release()
                
                cam_info = {
                    "index": idx,
                    "backend": b_name,
                    "stream_active": ret,
                    "default_resolution": [w, h],
                    "default_fps": fps,
                    "fourcc": fourcc_str,
                    "hd_capable": ret_hd and (hd_w == 1280 and hd_h == 720),
                    "tested_hd_resolution": [hd_w, hd_h] if ret_hd else None
                }
                cameras.append(cam_info)
                break  # Prefer the first working backend for this index
            cap.release()
            
    return cameras

def get_complete_camera_specification():
    """Consolidate hardware and software camera specifications."""
    wmi_cams = get_wmi_camera_info()
    cv_cams = probe_opencv_cameras()
    
    spec = {
        "timestamp": cv2.getTickCount(),
        "opencv_version": cv2.__version__,
        "platform": sys.platform,
        "hardware_sensors_detected": wmi_cams,
        "opencv_streams_probed": cv_cams,
        "primary_camera": cv_cams[0] if cv_cams else None,
        "status": "OPERATIONAL" if cv_cams and cv_cams[0].get("stream_active") else "NO_CAMERA_FOUND"
    }
    return spec

if __name__ == "__main__":
    print("=" * 60)
    print("CAMERA HARDWARE AUDIT & DISCOVERY")
    print("=" * 60)
    
    spec = get_complete_camera_specification()
    print(json.dumps(spec, indent=2))
    
    # Save to 01_camera_and_repo evidence folder
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_camera_and_repo"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "camera_specification.json")
    with open(out_file, "w") as f:
        json.dump(spec, f, indent=2)
    print(f"\n[+] Camera specifications successfully recorded to: {out_file}")

