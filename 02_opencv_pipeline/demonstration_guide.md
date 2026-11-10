# Pipeline Demonstration Guide

Step-by-step instructions to reproduce the live demonstration of Deliverable 2 on any host machine.

---

## 1. Running Mode A (Passthrough Baseline)
Mode A establishes the baseline video feed without running a neural network detector:

```powershell
# Run interactive live camera preview with HUD overlay
python pipeline/opencv_pipeline.py --mode A

# Run headless verification test (captures 20 frames and writes evidence)
python pipeline/opencv_pipeline.py --mode A --headless --frames 20 --save-screenshot 02_opencv_pipeline/mode_a_pipeline.jpg
```

---

## 2. Running Mode B (YOLO Enclosure Detector)
Mode B activates the single-class enclosure detection model:

```powershell
# Run live interactive detector with trained ONNX model
python pipeline/opencv_pipeline.py --mode B --model models/enclosure_yolo.onnx

# Run live detector using PyTorch/Ultralytics weights
python pipeline/opencv_pipeline.py --mode B --model models/enclosure_yolo.pt

# Run headless verification test
python pipeline/opencv_pipeline.py --mode B --model models/enclosure_yolo.onnx --headless --frames 20 --save-screenshot 02_opencv_pipeline/mode_b_pipeline.jpg
```

---

## 3. Interactive Keybindings
- **`q` or `ESC`:** Terminate the application cleanly and release the camera sensor.
- **`s`:** Save an instantaneous high-resolution annotated screenshot to disk.
