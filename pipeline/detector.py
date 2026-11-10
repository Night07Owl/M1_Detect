"""
YOLO Enclosure Detector Module
Multi-backend inference engine supporting ONNX Runtime, OpenCV DNN, and Ultralytics YOLO.
Target Class: 0 ('enclosure') - Rhino Motion RMCS-610 digital speed controller enclosure.
"""

import os
import cv2
import numpy as np

class EnclosureDetector:
    def __init__(self, model_path=None, conf_thres=0.35, iou_thres=0.45, input_size=(640, 640)):
        self.model_path = model_path
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.input_size = input_size
        self.classes = {0: "enclosure"}
        
        self.backend = None
        self.session = None
        self.net = None
        self.ultralytics_model = None
        
        if model_path and os.path.exists(model_path):
            self._load_model(model_path)
            
    def _load_model(self, model_path):
        ext = os.path.splitext(model_path)[1].lower()
        if ext == ".onnx":
            try:
                import onnxruntime as ort
                opts = ort.SessionOptions()
                opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                # Prefer DirectML / CUDA if available, fallback to CPU
                providers = ['CPUExecutionProvider']
                if 'DmlExecutionProvider' in ort.get_available_providers():
                    providers.insert(0, 'DmlExecutionProvider')
                elif 'CUDAExecutionProvider' in ort.get_available_providers():
                    providers.insert(0, 'CUDAExecutionProvider')
                    
                self.session = ort.InferenceSession(model_path, opts, providers=providers)
                self.backend = "onnxruntime"
                self.input_name = self.session.get_inputs()[0].name
                print(f"[+] Loaded ONNX model via onnxruntime ({self.session.get_providers()[0]}): {model_path}")
                return
            except Exception as e:
                print(f"[!] ONNX Runtime init failed ({e}), falling back to cv2.dnn...")
                
            try:
                self.net = cv2.dnn.readNetFromONNX(model_path)
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                self.backend = "opencv_dnn"
                print(f"[+] Loaded ONNX model via cv2.dnn: {model_path}")
                return
            except Exception as e:
                print(f"[-] Failed loading ONNX with cv2.dnn: {e}")
                
        elif ext in [".pt", ".yaml"]:
            try:
                from ultralytics import YOLO
                self.ultralytics_model = YOLO(model_path)
                self.backend = "ultralytics"
                print(f"[+] Loaded PyTorch/Ultralytics weights: {model_path}")
                return
            except Exception as e:
                print(f"[-] Ultralytics backend unavailable ({e})")
                
        self.backend = None
        print(f"[!] Warning: No active detector backend loaded for: {model_path}")

    def is_loaded(self):
        return self.backend is not None

    def _letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114)):
        shape = img.shape[:2]  # current shape [height, width]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw, dh = dw / 2, dh / 2
        
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return img, r, (dw, dh)

    def detect(self, frame):
        """
        Runs object detection on the input frame.
        Returns: list of detections, e.g.
        [{'box': [x1, y1, x2, y2], 'class_id': 0, 'class_name': 'enclosure', 'confidence': 0.92}]
        """
        if not self.is_loaded() or frame is None:
            return []
            
        orig_h, orig_w = frame.shape[:2]
        
        # 1. Ultralytics direct inference branch
        if self.backend == "ultralytics":
            results = self.ultralytics_model(frame, conf=self.conf_thres, iou=self.iou_thres, verbose=False)[0]
            detections = []
            if results.boxes is not None and len(results.boxes) > 0:
                for box in results.boxes:
                    cls_id = int(box.cls[0].item())
                    if cls_id == 0:  # Only class 0 ('enclosure')
                        coords = [float(v) for v in box.xyxy[0].tolist()]
                        conf = float(box.conf[0].item())
                        detections.append({
                            "box": coords,
                            "class_id": 0,
                            "class_name": "enclosure",
                            "confidence": round(conf, 4)
                        })
            return detections
            
        # 2. ONNX / OpenCV DNN inference branch
        input_img, ratio, (pad_w, pad_h) = self._letterbox(frame, self.input_size)
        blob = cv2.dnn.blobFromImage(input_img, 1.0 / 255.0, self.input_size, swapRB=True, crop=False)
        
        if self.backend == "onnxruntime":
            outputs = self.session.run(None, {self.input_name: blob})[0]
        elif self.backend == "opencv_dnn":
            self.net.setInput(blob)
            outputs = self.net.forward()
        else:
            return []
            
        # YOLOv8/v11 outputs shape: (1, 4 + num_classes, 8400)
        if outputs.ndim == 3 and outputs.shape[1] < outputs.shape[2]:
            outputs = np.transpose(outputs[0], (1, 0))  # (8400, 5)
        elif outputs.ndim == 3:
            outputs = outputs[0]
            
        boxes = []
        confidences = []
        class_ids = []
        
        for row in outputs:
            classes_scores = row[4:]
            class_id = int(np.argmax(classes_scores))
            score = float(classes_scores[class_id])
            
            if class_id == 0 and score >= self.conf_thres:
                cx, cy, w, h = row[0], row[1], row[2], row[3]
                
                # Transform coordinates back through letterbox padding
                x1 = (cx - w / 2 - pad_w) / ratio
                y1 = (cy - h / 2 - pad_h) / ratio
                x2 = (cx + w / 2 - pad_w) / ratio
                y2 = (cy + h / 2 - pad_h) / ratio
                
                # Clip to image bounds
                x1 = max(0, min(orig_w, x1))
                y1 = max(0, min(orig_h, y1))
                x2 = max(0, min(orig_w, x2))
                y2 = max(0, min(orig_h, y2))
                
                boxes.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
                confidences.append(float(score))
                class_ids.append(0)
                
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_thres, self.iou_thres)
        detections = []
        if len(indices) > 0:
            for idx in indices.flatten():
                bx, by, bw, bh = boxes[idx]
                detections.append({
                    "box": [bx, by, bx + bw, by + bh],
                    "class_id": 0,
                    "class_name": "enclosure",
                    "confidence": round(confidences[idx], 4)
                })
                
        return detections

