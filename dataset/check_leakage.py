"""
Dataset Data Leakage & Cross-Split Contamination Auditor
Verifies that no identical or visually near-duplicate images exist across
Train, Validation, and Test splits.
"""

import sys
import os
import glob
import hashlib
import json
import cv2

def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compute_dhash(image_path, hash_size=8):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        resized = cv2.resize(img, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
        diff = resized[:, 1:] > resized[:, :-1]
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    except Exception:
        return None

def hamming_distance(h1, h2):
    return bin(h1 ^ h2).count('1')

def check_dataset_leakage(images_dir="dataset/images"):
    splits = ["train", "val", "test"]
    split_files = {}
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    
    for s in splits:
        files = []
        for ext in valid_exts:
            files.extend(glob.glob(os.path.join(images_dir, s, ext)))
        split_files[s] = sorted(list(set(files)))
        
    counts = {s: len(split_files[s]) for s in splits}
    total = sum(counts.values())
    
    if total == 0:
        msg = f"Zero partitioned images found in '{images_dir}/[train|val|test]'. Status: PENDING DATA."
        report = {
            "status": "PENDING_DATA",
            "message": msg,
            "leakage_detected": False,
            "counts": counts,
            "exact_duplicate_violations": [],
            "near_duplicate_violations": []
        }
        _write_reports(report, msg)
        return report

    exact_duplicates = []
    near_duplicates = []
    
    # 1. Filename overlap check
    basenames = {s: set([os.path.basename(f) for f in split_files[s]]) for s in splits}
    train_val_overlap = basenames["train"].intersection(basenames["val"])
    train_test_overlap = basenames["train"].intersection(basenames["test"])
    val_test_overlap = basenames["val"].intersection(basenames["test"])
    
    filename_collisions = []
    if train_val_overlap:
        filename_collisions.append(f"Train-Val collision: {list(train_val_overlap)}")
    if train_test_overlap:
        filename_collisions.append(f"Train-Test collision: {list(train_test_overlap)}")
    if val_test_overlap:
        filename_collisions.append(f"Val-Test collision: {list(val_test_overlap)}")

    # 2. SHA-256 Hash Indexing
    sha_map = {}
    for s in splits:
        for f in split_files[s]:
            sha = compute_sha256(f)
            if sha in sha_map:
                prev_split, prev_f = sha_map[sha]
                if prev_split != s:
                    exact_duplicates.append({
                        "file_a": prev_f,
                        "split_a": prev_split,
                        "file_b": f,
                        "split_b": s,
                        "type": "exact_sha256_match"
                    })
            else:
                sha_map[sha] = (s, f)

    # 3. Perceptual Difference Hash Cross-Comparison
    dhashes = {s: [] for s in splits}
    for s in splits:
        for f in split_files[s]:
            dh = compute_dhash(f)
            if dh is not None:
                dhashes[s].append((f, dh))
                
    # Compare train vs val, train vs test, val vs test
    pairs = [("train", "val"), ("train", "test"), ("val", "test")]
    for s1, s2 in pairs:
        for f1, h1 in dhashes[s1]:
            for f2, h2 in dhashes[s2]:
                dist = hamming_distance(h1, h2)
                # Hamming distance <= 2 indicates virtually identical image
                if dist <= 2:
                    near_duplicates.append({
                        "file_a": f1,
                        "split_a": s1,
                        "file_b": f2,
                        "split_b": s2,
                        "hamming_distance": dist,
                        "type": "perceptual_near_duplicate"
                    })

    is_leakage = (len(exact_duplicates) > 0 or len(filename_collisions) > 0 or len(near_duplicates) > 0)
    
    report = {
        "status": "PASSED" if not is_leakage else "FAILED",
        "leakage_detected": is_leakage,
        "counts": counts,
        "total_images": total,
        "percentages": {s: round(counts[s] / total * 100.0, 1) for s in splits},
        "filename_collisions": filename_collisions,
        "exact_duplicate_violations": exact_duplicates,
        "near_duplicate_violations": near_duplicates
    }
    
    summary_text = (
        f"DATASET LEAKAGE AUDIT REPORT\n"
        f"Status: {report['status']}\n"
        f"Total Images: {total} (Train: {counts['train']}, Val: {counts['val']}, Test: {counts['test']})\n"
        f"Filename Overlaps: {len(filename_collisions)}\n"
        f"Exact Hash Duplicates Cross-Split: {len(exact_duplicates)}\n"
        f"Perceptual Near-Duplicates Cross-Split: {len(near_duplicates)}\n"
        f"Leakage Free: {'YES' if not is_leakage else 'NO - CONTAMINATION DETECTED'}\n"
    )
    _write_reports(report, summary_text)
    return report

def _write_reports(report_dict, summary_text):
    for d in ["05_correct_split", "results"]:
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "leakage_report.json"), "w") as f:
            json.dump(report_dict, f, indent=2)
        with open(os.path.join(d, "leakage_verification.txt"), "w") as f:
            f.write(summary_text)

if __name__ == "__main__":
    print("=" * 60)
    print("EXECUTING CROSS-SPLIT DATA LEAKAGE CHECK")
    print("=" * 60)
    rep = check_dataset_leakage()
    print(json.dumps(rep, indent=2))

