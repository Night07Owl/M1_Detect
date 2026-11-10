# OpenCV Pipeline Architecture Specification

## 1. Data Flow Architecture

```text
Physical Camera (DirectShow / UVC)
               │
               ▼
   [ Frame Capture (cap.read()) ]
               │
       ┌───────┴──────────────────┐
       ▼                          ▼
 [ MODE A: Passthrough ]   [ MODE B: Neural Detector ]
       │                          │
       │                   Letterbox Resizing (640x640)
       │                          │
       │                   Inference (ONNX / DNN)
       │                          │
       │                   NMS Suppression (IoU 0.45)
       │                          │
       └───────┬──────────────────┘
               │
               ▼
   [ Visualization & HUD Rendering ]
   (Bounding Box + Class + Conf + Latency + FPS)
               │
               ▼
      [ High-Speed Display Window ]
```

## 2. Telemetry and Latency Calculations
1. **Camera Acquisition Time:** $T_{\text{cap}} = t_{\text{read\_end}} - t_{\text{read\_start}}$
2. **Inference Latency:** $T_{\text{inf}} = t_{\text{nms\_end}} - t_{\text{letterbox\_start}}$
3. **Total Latency:** $T_{\text{tot}} = T_{\text{cap}} + T_{\text{inf}}$
4. **Instantaneous FPS:** Rolling harmonic mean over a 30-frame window.

## 3. Error Handling and Edge Cases
- **Device Disconnection:** Detects `ret is False` or empty frame buffer and terminates without crashing.
- **Resource Cleanup:** Guaranteed camera hardware release in `finally:` block.

