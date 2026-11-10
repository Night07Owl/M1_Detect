"""
Camera Live Capture Application & Frame Acquisition Engine
Supports both interactive GUI display and headless automated frame acquisition.
Saves genuine camera frames to evidence and dataset directories.
"""

import sys
import os
import time
import argparse
import json
import cv2

def capture_first_frame(cam_index=0, width=1280, height=720, save_path=None):
    """
    Capture a genuine first frame directly from the connected physical camera
    and write it to disk.
    """
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(cam_index, backend)
    
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera device index {cam_index}")
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Warm up automatic white balance and exposure
    for _ in range(5):
        cap.read()
        
    ret, frame = cap.read()
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    if not ret or frame is None:
        raise RuntimeError("Failed to capture frame from operational camera stream")
        
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        cv2.imwrite(save_path, frame)
        print(f"[+] Genuine frame captured and saved to: {save_path} ({actual_w}x{actual_h})")
        
    return frame, (actual_w, actual_h)

def run_interactive_camera(cam_index=0, width=1280, height=720, save_dir="dataset/raw_captures"):
    """
    Interactive live camera display mode.
    Keybindings:
      's': Save current frame with timestamp
      'q' or ESC: Quit cleanly
    """
    os.makedirs(save_dir, exist_ok=True)
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(cam_index, backend)
    
    if not cap.isOpened():
        print(f"[-] Error: Could not connect to camera {cam_index}")
        return
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[+] Camera active at {actual_w}x{actual_h}. Press 's' to capture, 'q' to exit.")
    
    frame_count = 0
    saved_count = 0
    prev_time = time.time()
    fps = 0.0
    
    window_name = "Live Camera Capture - Rhino Motion RMCS-610"
    try:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    except Exception as e:
        print(f"[!] Warning: GUI display not available ({e}). Running in headless test mode.")
        save_path = os.path.join(save_dir, "frame_0001.jpg")
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path, frame)
            print(f"[+] Saved headless frame: {save_path}")
        cap.release()
        return

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("[-] Camera stream interrupted. Exiting...")
            break
            
        frame_count += 1
        curr_time = time.time()
        elapsed = curr_time - prev_time
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            prev_time = curr_time
            
        # Draw HUD overlay
        overlay = frame.copy()
        cv2.putText(overlay, f"FPS: {fps:.1f} | Res: {actual_w}x{actual_h} | Saved: {saved_count}",
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.putText(overlay, "Keys: [S] Capture Frame | [Q] Exit",
                    (20, actual_h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 0), 2)
        
        cv2.imshow(window_name, overlay)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('s'):
            saved_count += 1
            filename = f"capture_{int(time.time())}_{saved_count:03d}.jpg"
            out_file = os.path.join(save_dir, filename)
            cv2.imwrite(out_file, frame)
            print(f"[+] Saved photograph: {out_file}")

    cap.release()
    cv2.destroyAllWindows()
    print("[+] Camera cleanly released.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camera Capture and Streaming Utility")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive GUI window")
    parser.add_argument("--index", type=int, default=0, help="Camera index")
    parser.add_argument("--width", type=int, default=1280, help="Resolution width")
    parser.add_argument("--height", type=int, default=720, help="Resolution height")
    parser.add_argument("--output", type=str, default="01_camera_and_repo/first_frame.jpg", help="Output frame path")
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive_camera(cam_index=args.index, width=args.width, height=args.height)
    else:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        save_path = os.path.join(root_dir, args.output)
        frame, (w, h) = capture_first_frame(cam_index=args.index, width=args.width, height=args.height, save_path=save_path)
        print(f"[SUCCESS] Acquired genuine frame of shape {frame.shape} at {w}x{h}")
