"""
Camera Live Capture Application & Frame Acquisition Engine
Supports interactive GUI display, automated interval burst capture, and headless frame acquisition.
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

def run_interactive_camera(cam_index=0, width=1280, height=720, save_dir="dataset/images",
                           auto_total=None, auto_interval=2.0, seq_name="seq01"):
    """
    Interactive live camera display mode.
    Supports manual capture on 's' or hands-free auto-interval capturing.
    Keybindings:
      's': Save current frame
      'space': Toggle auto-interval burst capture
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
    print(f"[+] Camera active at {actual_w}x{actual_h}. Saving to: {save_dir}")
    print(f"[+] Press 's' to capture single photo, 'Space' to toggle interval capture, 'q' to exit.")
    
    frame_count = 0
    saved_count = 0
    prev_time = time.time()
    last_auto_time = time.time()
    auto_active = (auto_total is not None and auto_total > 0)
    fps = 0.0
    
    window_name = "Live Camera Capture - Rhino Motion RMCS-610"
    try:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    except Exception as e:
        print(f"[!] Warning: GUI display not available ({e}). Running in headless test mode.")
        save_path = os.path.join(save_dir, f"{seq_name}_001.jpg")
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
            
        # Check auto interval capture
        if auto_active and (curr_time - last_auto_time >= auto_interval):
            saved_count += 1
            filename = f"{seq_name}_{int(time.time())}_{saved_count:03d}.jpg"
            out_file = os.path.join(save_dir, filename)
            cv2.imwrite(out_file, frame)
            print(f"[AUTO-CAPTURE {saved_count}/{auto_total or 'inf'}] Saved photograph: {out_file}")
            last_auto_time = curr_time
            if auto_total and saved_count >= auto_total:
                print(f"[+] Reached requested auto-capture count ({auto_total}). Stopping capture.")
                break
            
        # Draw HUD overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (actual_w, 42), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
        
        mode_str = f"AUTO ({saved_count}/{auto_total})" if auto_active else "MANUAL"
        cv2.putText(frame, f"FPS: {fps:.1f} | Res: {actual_w}x{actual_h} | Mode: {mode_str} | Saved: {saved_count}",
                    (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(frame, "[S] Capture Frame | [Space] Toggle Auto-Interval | [Q] Exit",
                    (15, actual_h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
        
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('s'):
            saved_count += 1
            filename = f"{seq_name}_{int(time.time())}_{saved_count:03d}.jpg"
            out_file = os.path.join(save_dir, filename)
            cv2.imwrite(out_file, frame)
            print(f"[+] Saved photograph: {out_file}")
        elif key == 32:  # Spacebar
            auto_active = not auto_active
            last_auto_time = curr_time
            print(f"[+] Auto interval capture toggled: {'ON' if auto_active else 'OFF'}")

    cap.release()
    cv2.destroyAllWindows()
    print(f"[+] Camera cleanly released. Total photographs saved: {saved_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camera Capture and Streaming Utility")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive GUI window")
    parser.add_argument("--index", type=int, default=0, help="Camera index")
    parser.add_argument("--width", type=int, default=1280, help="Resolution width")
    parser.add_argument("--height", type=int, default=720, help="Resolution height")
    parser.add_argument("--output", type=str, default="01_camera_and_repo/first_frame.jpg", help="Output frame path")
    parser.add_argument("--save-dir", type=str, default="dataset/images", help="Target folder for photographs")
    parser.add_argument("--auto", type=int, default=None, help="Auto-capture total frames")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between auto captures")
    parser.add_argument("--seq", type=str, default="seq01", help="Sequence prefix name")
    args = parser.parse_args()
    
    if args.interactive or args.auto is not None:
        run_interactive_camera(
            cam_index=args.index,
            width=args.width,
            height=args.height,
            save_dir=args.save_dir,
            auto_total=args.auto,
            auto_interval=args.interval,
            seq_name=args.seq
        )
    else:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        save_path = os.path.join(root_dir, args.output)
        frame, (w, h) = capture_first_frame(cam_index=args.index, width=args.width, height=args.height, save_path=save_path)
        print(f"[SUCCESS] Acquired genuine frame of shape {frame.shape} at {w}x{h}")
