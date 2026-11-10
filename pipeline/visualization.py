"""
OpenCV Visualization and HUD Overlay Engine
Renders professional bounding boxes, detection labels, confidence scores,
and real-time performance telemetry.
"""

import cv2
import numpy as np

CLASS_COLORS = {
    0: (0, 220, 110),       # Vibrant Green for 'enclosure'
    "default": (0, 165, 255) # Orange accent
}

def draw_hud(frame, mode, fps, latency_ms, enclosure_count, capture_ms=None):
    """
    Render top telemetry banner and status overlay.
    """
    h, w = frame.shape[:2]
    overlay = frame.copy()
    
    # Header bar background
    bar_height = 48
    cv2.rectangle(overlay, (0, 0), (w, bar_height), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    
    # Mode badge
    mode_text = f"MODE {mode}: {'YOLO ENCLOSURE DETECTOR' if mode == 'B' else 'OPENCV CAMERA PASSTHROUGH'}"
    mode_color = (0, 255, 128) if mode == 'B' else (0, 215, 255)
    cv2.putText(frame, mode_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, mode_color, 2, cv2.LINE_AA)
    
    # Telemetry text
    cap_str = f" | Cap: {capture_ms:.1f}ms" if capture_ms is not None else ""
    perf_text = f"FPS: {fps:.1f} | Latency: {latency_ms:.1f}ms{cap_str} | Enclosures: {enclosure_count}"
    
    # Calculate text width to right-align
    text_size = cv2.getTextSize(perf_text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)[0]
    tx = max(w - text_size[0] - 15, int(w * 0.45))
    cv2.putText(frame, perf_text, (tx, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Bottom keybinding hint bar
    footer_bar = frame.copy()
    cv2.rectangle(footer_bar, (0, h - 28), (w, h), (15, 15, 15), -1)
    cv2.addWeighted(footer_bar, 0.65, frame, 0.35, 0, frame)
    hint_text = "Target: Rhino Motion RMCS-610 | [Q] Quit | [S] Save Snapshot"
    cv2.putText(frame, hint_text, (15, h - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1, cv2.LINE_AA)
    
    return frame

def draw_detections(frame, detections):
    """
    Render bounding boxes, class names, and confidence percentages.
    detections: list of dicts:
      [{'box': [x1, y1, x2, y2], 'class_id': 0, 'class_name': 'enclosure', 'confidence': 0.94}, ...]
    """
    for det in detections:
        box = det["box"]
        x1, y1, x2, y2 = [int(v) for v in box]
        conf = det.get("confidence", 0.0)
        label = det.get("class_name", "enclosure")
        color = CLASS_COLORS.get(det.get("class_id", 0), CLASS_COLORS["default"])
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Corner accent highlights
        corner_len = min(16, (x2 - x1) // 4, (y2 - y1) // 4)
        if corner_len > 4:
            thick = 3
            # Top-left
            cv2.line(frame, (x1, y1), (x1 + corner_len, y1), color, thick)
            cv2.line(frame, (x1, y1), (x1, y1 + corner_len), color, thick)
            # Top-right
            cv2.line(frame, (x2, y1), (x2 - corner_len, y1), color, thick)
            cv2.line(frame, (x2, y1), (x2, y1 + corner_len), color, thick)
            # Bottom-left
            cv2.line(frame, (x1, y2), (x1 + corner_len, y2), color, thick)
            cv2.line(frame, (x1, y2), (x1, y2 - corner_len), color, thick)
            # Bottom-right
            cv2.line(frame, (x2, y2), (x2 - corner_len, y2), color, thick)
            cv2.line(frame, (x2, y2), (x2, y2 - corner_len), color, thick)
            
        # Label pill above bounding box
        caption = f"{label} {conf*100:.1f}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.55
        thickness = 1
        (txt_w, txt_h), baseline = cv2.getTextSize(caption, font, font_scale, thickness)
        
        py1 = max(y1 - txt_h - 8, 0)
        py2 = py1 + txt_h + 8
        px1 = x1
        px2 = x1 + txt_w + 10
        
        cv2.rectangle(frame, (px1, py1), (px2, py2), color, -1)
        cv2.putText(frame, caption, (px1 + 5, py2 - 5), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
        
    return frame
