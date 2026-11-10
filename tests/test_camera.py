"""
Test Suite: Camera Discovery & Capture Verification
"""

import os
import cv2
import numpy as np
import pytest
from camera.camera_info import probe_opencv_cameras, get_complete_camera_specification
from camera.camera_test import test_invalid_camera_handling as check_invalid_camera
from camera.camera_test import test_camera_connection as check_camera_connection

def test_camera_invalid_index_handling():
    """Verify system safely rejects non-existent camera index."""
    res = check_invalid_camera()
    assert res["correctly_rejected"] is True
    assert res["handled_gracefully"] is True

def test_camera_spec_generation():
    """Verify camera specification dictionary schema."""
    spec = get_complete_camera_specification()
    assert "opencv_version" in spec
    assert "platform" in spec
    assert "status" in spec

def test_camera_hardware_connection():
    """Verify physical camera connection if hardware available."""
    res = check_camera_connection(cam_index=0)
    if not res.get("success"):
        pytest.skip("Physical camera unavailable in current environment")
    assert res["actual_resolution"][0] > 0
    assert res["actual_resolution"][1] > 0
    assert res["valid_frame"] is True
