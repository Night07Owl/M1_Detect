"""
Local YOLO Image Annotation Utility
Provides an interactive OpenCV interface and programmatic API for labeling
the Rhino Motion RMCS-610 digital speed controller enclosure (Class ID: 0).
"""

import sys
import os
import glob
import cv2

def convert_to_yolo(box_xyxy, img_width, img_height, class_id=0):
    """Convert absolute [x1, y1, x2, y2] to normalized [class_id, xc, yc, w, h]."""
    x1, y1, x2, y2 = box_xyxy
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    
    # Clip to image bounds
    xmin = max(0, min(img_width, xmin))
    xmax = max(0, min(img_width, xmax))
    ymin = max(0, min(img_height, ymin))
    ymax = max(0, min(img_height, ymax))
    
    w_box = xmax - xmin
    h_box = ymax - ymin
    if w_box <= 0 or h_box <= 0:
        return None
        
    xc = (xmin + xmax) / 2.0 / img_width
    yc = (ymin + ymax) / 2.0 / img_height
    norm_w = w_box / float(img_width)
    norm_h = h_box / float(img_height)
    
    return [class_id, round(xc, 6), round(yc, 6), round(norm_w, 6), round(norm_h, 6)]

def convert_from_yolo(yolo_line, img_width, img_height):
    """Convert normalized [class_id, xc, yc, w, h] to absolute [x1, y1, x2, y2]."""
    parts = yolo_line.strip().split()
    if len(parts) < 5:
        return None
    cls_id = int(parts[0])
    xc, yc, w, h = [float(v) for v in parts[1:5]]
    
    xmin = int((xc - w / 2.0) * img_width)
    ymin = int((yc - h / 2.0) * img_height)
    xmax = int((xc + w / 2.0) * img_width)
    ymax = int((yc + h / 2.0) * img_height)
    return {"class_id": cls_id, "box": [xmin, ymin, xmax, ymax]}

class InteractiveAnnotator:
    def __init__(self, images_dir="dataset/images", labels_dir="dataset/labels"):
        self.images_dir = images_dir
        self.labels_dir = labels_dir
        os.makedirs(labels_dir, exist_ok=True)
        
        valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
        self.image_files = []
        for ext in valid_exts:
            self.image_files.extend(glob.glob(os.path.join(images_dir, ext)))
            self.image_files.extend(glob.glob(os.path.join(images_dir, "**", ext), recursive=True))
        self.image_files = sorted(list(set(self.image_files)))
        
        self.current_idx = 0
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.current_rect = None
        self.boxes = []
        
    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.current_rect = [x, y, x, y]
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.current_rect = [self.ix, self.iy, x, y]
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.current_rect = [self.ix, self.iy, x, y]
            x1, y1, x2, y2 = self.current_rect
            if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:
                self.boxes.append([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)])
            self.current_rect = None

    def run(self):
        if not self.image_files:
            print(f"[!] No images found in {self.images_dir}. Please place real camera photographs to annotate.")
            return
            
        cv2.namedWindow("RMCS-610 Annotator", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("RMCS-610 Annotator", self._mouse_callback)
        
        while 0 <= self.current_idx < len(self.image_files):
            img_path = self.image_files[self.current_idx]
            img = cv2.imread(img_path)
            if img is None:
                self.current_idx += 1
                continue
                
            h, w = img.shape[:2]
            label_file = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
            label_path = os.path.join(self.labels_dir, label_file)
            
            # Load existing boxes if not already loaded
            self.boxes = []
            if os.path.exists(label_path):
                with open(label_path, "r") as f:
                    for line in f:
                        b = convert_from_yolo(line, w, h)
                        if b:
                            self.boxes.append(b["box"])
                            
            while True:
                display = img.copy()
                # Draw existing boxes
                for box in self.boxes:
                    cv2.rectangle(display, (box[0], box[1]), (box[2], box[3]), (0, 220, 100), 2)
                    cv2.putText(display, "enclosure (0)", (box[0], max(15, box[1] - 5)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 100), 1)
                                
                # Draw current active box
                if self.drawing and self.current_rect:
                    r = self.current_rect
                    cv2.rectangle(display, (r[0], r[1]), (r[2], r[3]), (0, 200, 255), 1)
                    
                # HUD Header
                header_text = f"[{self.current_idx + 1}/{len(self.image_files)}] {os.path.basename(img_path)} | Boxes: {len(self.boxes)}"
                cv2.putText(display, header_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
                cv2.putText(display, "[S] Save & Next | [U] Undo Last | [C] Clear | [Q] Quit",
                            (10, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                cv2.imshow("RMCS-610 Annotator", display)
                key = cv2.waitKey(20) & 0xFF
                if key == ord('s'):
                    # Save annotations
                    with open(label_path, "w") as f:
                        for box in self.boxes:
                            yolo_coords = convert_to_yolo(box, w, h, class_id=0)
                            if yolo_coords:
                                f.write(" ".join(str(v) for v in yolo_coords) + "\n")
                    print(f"[+] Saved {len(self.boxes)} boxes to: {label_path}")
                    self.current_idx += 1
                    break
                elif key == ord('u'):
                    if self.boxes:
                        self.boxes.pop()
                elif key == ord('c'):
                    self.boxes = []
                elif key == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    return

        cv2.destroyAllWindows()

if __name__ == "__main__":
    annotator = InteractiveAnnotator()
    annotator.run()
