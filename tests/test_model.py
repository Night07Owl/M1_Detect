"""
Test Suite: ONNX Model Loading, Shape Consistency, and Edge Inference
"""

import os
import onnx
import onnxruntime as ort
from pipeline.detector import EnclosureDetector

def test_base_onnx_model_validity():
    model_path = "models/enclosure_detector_base.onnx"
    assert os.path.exists(model_path), "Base ONNX model missing"
    
    # Check ONNX graph validity
    model = onnx.load(model_path)
    onnx.checker.check_model(model)
    
    # Check input and output names
    session = ort.InferenceSession(model_path)
    inputs = session.get_inputs()
    outputs = session.get_outputs()
    assert inputs[0].name == "images"
    assert outputs[0].name == "output0"
    assert outputs[0].shape == [1, 5, 8400]

def test_detector_backend_loading():
    det = EnclosureDetector(model_path="models/enclosure_detector_base.onnx")
    assert det.is_loaded() is True
    assert det.backend in ["onnxruntime", "opencv_dnn"]

