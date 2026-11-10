"""
CAD Inspection and Analysis Tool
Extracts structural and geometric metadata from STEP and STL files for
the Rhino Motion RMCS-610 digital speed controller enclosure.
"""

import os
import struct
import re
import json

def parse_stl(stl_path):
    if not os.path.exists(stl_path):
        return {"error": f"File not found: {stl_path}"}
    
    file_size = os.path.getsize(stl_path)
    with open(stl_path, "rb") as f:
        header = f.read(80)
        num_triangles_bytes = f.read(4)
        if len(num_triangles_bytes) < 4:
            return {"error": "Invalid STL file"}
        num_triangles = struct.unpack("<I", num_triangles_bytes)[0]
        
        expected_size = 84 + num_triangles * 50
        is_size_valid = (file_size == expected_size)
        
        min_x = min_y = min_z = float("inf")
        max_x = max_y = max_z = float("-inf")
        
        for _ in range(num_triangles):
            # normal (3 floats), v1 (3 floats), v2 (3 floats), v3 (3 floats), attr (uint16)
            data = f.read(50)
            if len(data) < 50:
                break
            values = struct.unpack("<12fH", data)
            # vertices are at index 3..11
            for i in range(3, 12, 3):
                x, y, z = values[i], values[i+1], values[i+2]
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                min_z = min(min_z, z)
                max_z = max(max_z, z)
                
    dims = {
        "x_length_mm": round(max_x - min_x, 3),
        "y_width_mm": round(max_y - min_y, 3),
        "z_height_mm": round(max_z - min_z, 3),
    }
    
    return {
        "file_path": stl_path,
        "file_size_bytes": file_size,
        "format": "Binary STL",
        "header_ascii": header.decode("ascii", errors="replace").strip(),
        "triangle_count": num_triangles,
        "size_matches_triangle_count": is_size_valid,
        "bounding_box": {
            "min": [round(min_x, 3), round(min_y, 3), round(min_z, 3)],
            "max": [round(max_x, 3), round(max_y, 3), round(max_z, 3)],
        },
        "dimensions_mm": dims
    }

def parse_step(step_path):
    if not os.path.exists(step_path):
        return {"error": f"File not found: {step_path}"}
    
    with open(step_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        
    solid_breps = re.findall(r"MANIFOLD_SOLID_BREP\s*\(\s*'([^']*)'", content)
    products = re.findall(r"PRODUCT\s*\(\s*'([^']*)',\s*'([^']*)'", content)
    units = re.findall(r"SI_UNIT\s*\(\s*([^\)]*)\)", content)
    
    # Extract Cartesian points
    pts = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-+0-9.eE]+)\s*,\s*([-+0-9.eE]+)\s*,\s*([-+0-9.eE]+)\s*\)\s*\)", content)
    if pts:
        xs = [float(p[0]) for p in pts]
        ys = [float(p[1]) for p in pts]
        zs = [float(p[2]) for p in pts]
        bbox = {
            "min": [round(min(xs), 3), round(min(ys), 3), round(min(zs), 3)],
            "max": [round(max(xs), 3), round(max(ys), 3), round(max(zs), 3)],
            "dimensions_mm": {
                "x_length_mm": round(max(xs) - min(xs), 3),
                "y_width_mm": round(max(ys) - min(ys), 3),
                "z_height_mm": round(max(zs) - min(zs), 3)
            }
        }
    else:
        bbox = None
        
    return {
        "file_path": step_path,
        "file_size_bytes": os.path.getsize(step_path),
        "total_lines": content.count("\n"),
        "solid_bodies": solid_breps,
        "product_names": [p[1] for p in products],
        "units": units,
        "cartesian_points_count": len(pts),
        "cartesian_bounding_box": bbox
    }

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    stl_file = os.path.join(base_dir, "cad", "original", "Rhino+Motion+RMCS-610+digital+speed+controller.stl")
    step_file = os.path.join(base_dir, "cad", "original", "Rhino+Motion+RMCS-610+digital+speed+controller.stp")
    
    print("--- STL ANALYSIS ---")
    stl_res = parse_stl(stl_file)
    print(json.dumps(stl_res, indent=2))
    
    print("\n--- STEP ANALYSIS ---")
    step_res = parse_step(step_file)
    print(json.dumps(step_res, indent=2))
    
    analysis_dir = os.path.join(base_dir, "cad", "analysis")
    os.makedirs(analysis_dir, exist_ok=True)
    with open(os.path.join(analysis_dir, "cad_geometry_summary.json"), "w") as out:
        json.dump({"stl": stl_res, "step": step_res}, out, indent=2)
    print(f"\nSaved analysis to {os.path.join(analysis_dir, 'cad_geometry_summary.json')}")
