"""
YOLO Dataset Splitter (70% Train / 20% Val / 10% Test)
Enforces sequence/burst grouping to prevent data leakage between splits.
Generates distribution report and visual distribution chart.
"""

import sys
import os
import glob
import shutil
import json
import random
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def get_sequence_key(filename):
    """
    Extract sequence/burst prefix to ensure temporally correlated captures
    stay in the same split partition.
    E.g. 'seq01_angle_front_001.jpg' -> 'seq01'
         'capture_17312345_01.jpg' -> 'capture_17312345'
    """
    base = os.path.splitext(filename)[0]
    match = re.match(r"(seq\d+|burst\d+|capture_\d+)", base, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    # If no explicit sequence prefix, group by base angle prefix
    parts = base.split("_")
    if len(parts) > 1:
        return parts[0]
    return base

def split_dataset(images_dir="dataset/images", labels_dir="dataset/labels",
                  train_ratio=0.70, val_ratio=0.20, test_ratio=0.10, seed=42):
    random.seed(seed)
    
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    all_images = []
    for ext in valid_exts:
        # Only take images directly under images_dir (not already split subdirs)
        all_images.extend(glob.glob(os.path.join(images_dir, ext)))
    all_images = sorted(list(set(all_images)))
    
    total_imgs = len(all_images)
    if total_imgs == 0:
        # Check if already partitioned into train/val/test
        train_imgs = glob.glob(os.path.join(images_dir, "train", "*.*"))
        val_imgs = glob.glob(os.path.join(images_dir, "val", "*.*"))
        test_imgs = glob.glob(os.path.join(images_dir, "test", "*.*"))
        total_partitioned = len(train_imgs) + len(val_imgs) + len(test_imgs)
        
        if total_partitioned > 0:
            print(f"[+] Dataset already partitioned: Train={len(train_imgs)}, Val={len(val_imgs)}, Test={len(test_imgs)}")
            return _export_split_summary(len(train_imgs), len(val_imgs), len(test_imgs), seed)
        else:
            print(f"[!] Warning: No images found to split in '{images_dir}'. Status: PENDING DATA.")
            return {
                "status": "PENDING_DATA",
                "message": "Zero photographs available. Please capture and place physical RMCS-610 enclosure images."
            }

    # Group by sequence key
    groups = {}
    for img_path in all_images:
        fname = os.path.basename(img_path)
        key = get_sequence_key(fname)
        groups.setdefault(key, []).append(img_path)
        
    group_keys = list(groups.keys())
    random.shuffle(group_keys)
    
    train_imgs, val_imgs, test_imgs = [], [], []
    target_train = int(round(total_imgs * train_ratio))
    target_val = int(round(total_imgs * val_ratio))
    
    for key in group_keys:
        items = groups[key]
        if len(train_imgs) + len(items) <= target_train or (len(val_imgs) >= target_val and len(test_imgs) >= (total_imgs - target_train - target_val)):
            train_imgs.extend(items)
        elif len(val_imgs) + len(items) <= target_val:
            val_imgs.extend(items)
        else:
            test_imgs.extend(items)
            
    # Guarantee test set is non-empty if total_imgs >= 10
    if len(test_imgs) == 0 and len(train_imgs) > 1:
        test_imgs.append(train_imgs.pop())
    if len(val_imgs) == 0 and len(train_imgs) > 1:
        val_imgs.append(train_imgs.pop())
        
    # Create target directories
    for split_name, img_list in [("train", train_imgs), ("val", val_imgs), ("test", test_imgs)]:
        target_img_dir = os.path.join(images_dir, split_name)
        target_lbl_dir = os.path.join(labels_dir, split_name)
        os.makedirs(target_img_dir, exist_ok=True)
        os.makedirs(target_lbl_dir, exist_ok=True)
        
        for src_img in img_list:
            base = os.path.splitext(os.path.basename(src_img))[0]
            shutil.move(src_img, os.path.join(target_img_dir, os.path.basename(src_img)))
            
            src_lbl = os.path.join(labels_dir, f"{base}.txt")
            if os.path.exists(src_lbl):
                shutil.move(src_lbl, os.path.join(target_lbl_dir, f"{base}.txt"))
                
    return _export_split_summary(len(train_imgs), len(val_imgs), len(test_imgs), seed)

def _export_split_summary(n_train, n_val, n_test, seed):
    total = n_train + n_val + n_test
    p_train = round(n_train / total * 100.0, 1) if total > 0 else 0.0
    p_val = round(n_val / total * 100.0, 1) if total > 0 else 0.0
    p_test = round(n_test / total * 100.0, 1) if total > 0 else 0.0
    
    summary = {
        "status": "COMPLETE" if total > 0 else "PENDING_DATA",
        "random_seed": seed,
        "total_images": total,
        "split_counts": {
            "train": n_train,
            "val": n_val,
            "test": n_test
        },
        "split_percentages": {
            "train": p_train,
            "val": p_val,
            "test": p_test
        },
        "target_ratios": {
            "train": 70.0,
            "val": 20.0,
            "test": 10.0
        }
    }
    
    # Save chart
    _generate_split_chart(n_train, n_val, n_test, p_train, p_val, p_test)
    
    # Save json reports
    for out_p in ["05_correct_split/split_summary.json", "results/split_summary.json"]:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        with open(out_p, "w") as f:
            json.dump(summary, f, indent=2)
            
    return summary

def _generate_split_chart(n_train, n_val, n_test, p_train, p_val, p_test):
    labels = [f"Train (70%)\n{n_train} imgs ({p_train}%)",
              f"Val (20%)\n{n_val} imgs ({p_val}%)",
              f"Test (10%)\n{n_test} imgs ({p_test}%)"]
    sizes = [n_train if n_train > 0 else 70,
             n_val if n_val > 0 else 20,
             n_test if n_test > 0 else 10]
    colors = ["#2b8a3e", "#228be6", "#e67700"]
    explode = (0.05, 0.05, 0.05)
    
    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                      startangle=140, colors=colors, textprops=dict(color="black", fontsize=11))
    ax.set_title("Rhino Motion RMCS-610 Dataset Partition (70/20/10 Split)", fontsize=13, fontweight="bold")
    
    plt.tight_layout()
    for dest in ["05_correct_split/split_distribution.png", "results/split_distribution.png"]:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        fig.savefig(dest, dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    res = split_dataset()
    print(json.dumps(res, indent=2))
