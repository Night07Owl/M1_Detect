"""
Test Suite: Dataset Partitioning & Cross-Split Contamination Audit
"""

import os
from dataset.split_dataset import get_sequence_key
from dataset.check_leakage import check_dataset_leakage

def test_sequence_key_grouping():
    assert get_sequence_key("seq01_angle_front_001.jpg") == "seq01"
    assert get_sequence_key("burst05_top_04.png") == "burst05"
    assert get_sequence_key("capture_17312345_001.jpg") == "capture_17312345"
    assert get_sequence_key("front_angle_01.jpg") == "front"

def test_leakage_audit_pending_or_passed():
    rep = check_dataset_leakage()
    # In pending or populated state, leakage must be False
    assert rep["leakage_detected"] is False
    assert rep["status"] in ["PASSED", "PENDING_DATA"]

