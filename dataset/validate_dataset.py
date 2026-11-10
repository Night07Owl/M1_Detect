"""
YOLO Dataset Quality & Integrity Validator
Performs rigorous verification on image-label consistency, class IDs,
normalized coordinate bounds, degenerate boxes, and duplicate images.
"""

import sys
import os
import glob
import hashlib
import json
import cv2
import numpy as np

def compute_image_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compute_dhash(image_path, hash_size=8):
    """Compute difference hash (dHash) to identify visually identical or near-duplicate images."""
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        resized = cv2.resize(img, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
        diff = resized[:, 1:] > resized[:, :-1]
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    except Exception:
        return None

def validate_dataset(images_dir="dataset/images", labels_dir="dataset/labels"):
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    image_files = []
    for ext in valid_exts:
        image_files.extend(glob.glob(os.path.join(images_dir, ext)))
        image_files.extend(glob.glob(os.path.join(images_dir, "**", ext), recursive=True))
    image_files = sorted(list(set(image_files)))
    
    total_images = len(image_files)
    if total_images == 0:
        return {
            "status": "PENDING_DATA",
            "message": f"Zero photographic images found in '{images_dir}'. Dataset requires physical camera captures.",
            "total_images": 0,
            "total_labels": 0,
            "errors": []
        }
        
    errors = []
    warnings = []
    class_counts = {0: 0}
    total_boxes = 0
    
    # Track hashes for duplicates
    sha256_map = {}
    dhash_map = {}
    duplicates = []
    
    for img_path in image_files:
        # Check image corruption
        img = cv2.imread(img_path)
        if img is None:
            errors.append({"file": img_path, "error": "Corrupted or unreadable image file"})
            continue
            
        # Check duplicate
        sha = compute_image_sha256(img_path)
        if sha in sha256_map:
            duplicates.append({"original": sha256_map[sha], "duplicate": img_path, "type": "identical_sha256"})
        else:
            sha256_map[sha] = img_path
            
        dh = compute_dhash(img_path)
        if dh is not None:
            if dh in dhash_map:
                duplicates.append({"original": dhash_map[dh], "near_duplicate": img_path, "type": "perceptual_dhash"})
            else:
                dhash_map[dh] = img_path
                
        # Find corresponding label
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        # Check in labels_dir or parallel labels path
        label_path = os.path.join(labels_dir, f"{base_name}.txt")
        if not os.path.exists(label_path):
            # Check parallel folder if split
            rel_dir = os.path.relpath(os.path.dirname(img_path), images_dir)
            alt_label_path = os.path.join(labels_dir, rel_dir, f"{base_name}.txt")
            if os.path.exists(alt_label_path):
                label_path = alt_label_path
            else:
                warnings.append({"file": img_path, "warning": "Missing corresponding YOLO label file"})
                continue
                
        with open(label_path, "r", encoding="utf-8") as lf:
            lines = [line.strip() for line in lf if line.strip()]
            
        if len(lines) == 0:
            warnings.append({"file": label_path, "warning": "Empty label file (background image or unannotated)"})
            continue
            
        for line_num, line in enumerate(lines, 1):
            parts = line.split()
            if len(parts) != 5:
                errors.append({"file": label_path, "line": line_num, "error": f"Invalid YOLO format (expected 5 tokens, got {len(parts)})"})
                continue
                
            try:
                cls_id = int(parts[0])
                xc, yc, w, h = [float(v) for v in parts[1:5]]
            except ValueError:
                errors.append({"file": label_path, "line": line_num, "error": "Non-numeric token in bounding box"})
                continue
                
            # Class validation
            if cls_id != 0:
                errors.append({"file": label_path, "line": line_num, "error": f"Invalid Class ID {cls_id} (Only Class 0: 'enclosure' permitted)"})
            else:
                class_counts[0] = class_counts.get(0, 0) + 1
                total_boxes += 1
                
            # Range validation [0, 1]
            if not (0.0 <= xc <= 1.0 and 0.0 <= yc <= 1.0):
                errors.append({"file": label_path, "line": line_num, "error": f"Center coordinates ({xc}, {yc}) outside normalized bounds [0, 1]"})
            if not (0.0 < w <= 1.0 and 0.0 < h <= 1.0):
                errors.append({"file": label_path, "line": line_num, "error": f"Box dimensions ({w}, {h}) zero, negative, or exceeding 1.0"})
                
            # Check for inverted or clipping boxes
            if (xc - w/2.0 < -0.05) or (xc + w/2.0 > 1.05) or (yc - h/2.0 < -0.05) or (yc + h/2.0 > 1.05):
                errors.append({"file": label_path, "line": line_num, "error": "Bounding box significantly clips beyond image margins"})
                
    result = {
        "status": "PASSED" if len(errors) == 0 else "FAILED",
        "total_images": total_images,
        "total_boxes_annotated": total_boxes,
        "class_distribution": class_counts,
        "identical_duplicates_count": len(duplicates),
        "duplicates": duplicates,
        "errors_count": len(errors),
        "warnings_count": len(warnings),
        "errors": errors,
        "warnings": warnings
    }
    return result

if __name__ == "__main__":
    print("=" * 60)
    print("YOLO DATASET QUALITY & INTEGRITY VALIDATION")
    print("=" * 60)
    res = validate_dataset()
    print(json.dumps(res, indent=2))
    
    out_dir = "04_dataset_v1"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "validation_report.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n[+] Validation report exported to: {os.path.join(out_dir, 'validation_report.json')}")

