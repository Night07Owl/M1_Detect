# Setup & Reproduction Instructions

This document provides exact steps to reproduce Deliverable 1 on any Windows or Edge computing environment.

## 1. Prerequisites
- Python 3.11+ 64-bit
- Git 2.40+
- USB or Integrated Camera device

## 2. Environment Setup
```powershell
# 1. Clone repository
git clone <YOUR_REPO_URL>
cd "Edge AI - Assignment 1"

# 2. Create isolated virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install project dependencies
pip install -r requirements.txt
```

## 3. Camera Discovery & Frame Verification
```powershell
# Query camera properties and hardware IDs
python camera/camera_info.py

# Run camera connection and FPS benchmark test
python camera/camera_test.py

# Capture genuine first frame
python camera/camera_capture.py --output 01_camera_and_repo/first_frame.jpg

# Optional: Run live interactive camera preview
python camera/camera_capture.py --interactive
```
