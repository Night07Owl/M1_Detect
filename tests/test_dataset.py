"""
Test Suite: YOLO Dataset Conversion, Bounding Box Validation, and Duplicate Detection
"""

import pytest
from dataset.annotate_dataset import convert_to_yolo, convert_from_yolo
from dataset.validate_dataset import compute_image_sha256

def test_yolo_coordinate_conversion():
    # Image size 1000 x 500, Box [100, 100, 300, 300]
    # xc = 200/1000 = 0.2, yc = 200/500 = 0.4, w = 200/1000 = 0.2, h = 200/500 = 0.4
    yolo = convert_to_yolo([100, 100, 300, 300], 1000, 500, class_id=0)
    assert yolo[0] == 0
    assert yolo[1] == pytest.approx(0.2, rel=1e-3)
    assert yolo[2] == pytest.approx(0.4, rel=1e-3)
    assert yolo[3] == pytest.approx(0.2, rel=1e-3)
    assert yolo[4] == pytest.approx(0.4, rel=1e-3)
    
    # Invert conversion
    line = "0 0.2 0.4 0.2 0.4"
    inv = convert_from_yolo(line, 1000, 500)
    assert inv["class_id"] == 0
    assert inv["box"] == [100, 100, 300, 300]

def test_degenerate_box_rejection():
    # Inverted or zero box
    yolo = convert_to_yolo([100, 100, 100, 100], 1000, 500, class_id=0)
    assert yolo is None

