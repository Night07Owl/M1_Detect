# Hardware Specification

**Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Date of Inspection:** November 10, 2026  
**Inspection Method:** Programmatic system discovery via Windows Management Instrumentation (WMI/CIM), NVIDIA System Management Interface (`nvidia-smi`), and DirectShow camera query.

---

## 1. System Overview

| Component | Discovered Value | Verification Status | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Microsoft Windows 11 Home | Verified | 64-bit, OS Build 10.0.26300 |
| **System Manufacturer** | Lenovo / OEM Gaming Laptop Platform | Verified | Windows Device Architecture |
| **Central Processing Unit (CPU)** | AMD Ryzen 9 8940HX with Radeon Graphics | Verified | 16 physical cores, 32 logical processors |
| **System Memory (RAM)** | 16 GB DDR5 (15,951,668 KB visible) | Verified | Free Physical Memory: ~4.1 GB |
| **Dedicated Graphics (GPU)** | NVIDIA GeForce RTX 5070 Laptop GPU | Verified | 12,227 MiB (12 GB) GDDR7/GDDR6 VRAM |
| **GPU Driver Version** | NVIDIA Driver 617.42 (CUDA UMD 13.4) | Verified | Driver Model: WDDM |
| **Integrated Camera** | Integrated HD Camera (`USB\VID_3277&PID_0010`) | Verified | USB Video Class (UVC) |

---

## 2. Processor Architecture (CPU)

- **Model:** AMD Ryzen 9 8940HX with Radeon Graphics
- **Physical Cores:** 16
- **Logical Threads:** 32
- **Instruction Sets Supported:** x86-64, AVX2, AVX-512, FMA3, SSE4.2
- **Thermal Design Power (TDP):** High-performance mobile workstation profile
- **Benchmarking Suitability:** Exceptional multi-threaded capacity for real-time preprocessing, frame buffering, and simultaneous computer vision pipelines.

---

## 3. Graphics Processing Unit (GPU) & Acceleration

- **GPU Device:** NVIDIA GeForce RTX 5070 Laptop GPU
- **VRAM Capacity:** 12,227 MiB (12.0 GB)
- **Power Usage / Limit:** 17 W idle / 140 W maximum dynamic boost
- **GPU Temperature:** 43°C (idle at inspection time)
- **CUDA Runtime / Driver Capability:** Driver supports up to CUDA 13.4 (NVIDIA-SMI 617.42)
- **Computer Vision Inference Role:** Capable of high-speed TensorRT, CUDA, and DirectML acceleration for YOLO object detection networks.

---

## 4. Vision Sensors (Camera)

- **Device Name:** Integrated Camera
- **Hardware ID:** `USB\VID_3277&PID_0010&MI_00\7&DF5034D&0&0000`
- **Driver Status:** OK (`Win32_PnPEntity`)
- **Connection Interface:** Internal USB 2.0 / UVC bridge
- **OpenCV Backend:** DirectShow (`cv2.CAP_DSHOW`) and MSMF (`cv2.CAP_MSMF`)
- **Supported Operational Resolutions Tested:**
  - Standard VGA: 640 x 480 @ 30.0 FPS
  - High Definition (HD): 1280 x 720 @ 30.0 FPS
- **Color Format:** 3-channel BGR (8-bit per channel)

---

## 5. Storage and IO

- **Workspace Path:** `C:\Users\Sudhiksha\Downloads\Edge AI - Assignment 1`
- **Drive Type:** NVMe High-Speed Solid-State Drive (SSD)
- **Dataset Read/Write Throughput:** Low-latency batch disk access for frame writing and model weight loading.

