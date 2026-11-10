"""
Test Suite: CAD Inspection & Dimensional Verification
"""

import os
import pytest
from cad.inspect_cad import parse_stl, parse_step

@pytest.fixture
def cad_paths():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    stl_path = os.path.join(base_dir, "cad", "original", "Rhino+Motion+RMCS-610+digital+speed+controller.stl")
    step_path = os.path.join(base_dir, "cad", "original", "Rhino+Motion+RMCS-610+digital+speed+controller.stp")
    return stl_path, step_path

def test_stl_parsing(cad_paths):
    stl_path, _ = cad_paths
    assert os.path.exists(stl_path), f"STL file missing at {stl_path}"
    
    result = parse_stl(stl_path)
    assert result["format"] == "Binary STL"
    assert result["triangle_count"] == 1048
    assert result["size_matches_triangle_count"] is True
    
    # Check dimensions match physical envelope (81.5 x 73.7 x 18.0 mm)
    dims = result["dimensions_mm"]
    assert dims["x_length_mm"] == pytest.approx(81.5, rel=1e-2)
    assert dims["y_width_mm"] == pytest.approx(73.7, rel=1e-2)
    assert dims["z_height_mm"] == pytest.approx(18.0, rel=1e-2)

def test_step_parsing(cad_paths):
    _, step_path = cad_paths
    assert os.path.exists(step_path), f"STEP file missing at {step_path}"
    
    result = parse_step(step_path)
    # Check 3 named solid bodies exist
    assert "top" in result["solid_bodies"]
    assert "bottom" in result["solid_bodies"]
    assert "component" in result["solid_bodies"]
    assert len(result["solid_bodies"]) == 3
    
    # Check Cartesian bounding box matches STL
    c_dims = result["cartesian_bounding_box"]["dimensions_mm"]
    assert c_dims["x_length_mm"] == pytest.approx(81.5, rel=1e-2)
    assert c_dims["y_width_mm"] == pytest.approx(73.7, rel=1e-2)
    assert c_dims["z_height_mm"] == pytest.approx(18.0, rel=1e-2)

