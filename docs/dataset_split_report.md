# Dataset Partition & Data Leakage Audit Report

**Project:** Rhino Motion RMCS-610 Digital Speed Controller Enclosure Detection  
**Target Split:** Strict 70% Training / 20% Validation / 10% Testing  
**Auditor Engine:** `dataset/check_leakage.py` & `dataset/split_dataset.py`  
**Date:** November 10, 2026  

---

## 1. Split Partitioning Architecture

To guarantee unbiased model generalization, the dataset partitioning pipeline enforces strict sequence isolation:

```text
       Raw Physical Image Captures
                   │
                   ▼
     [ Sequence / Burst Key Grouping ]
     (e.g., 'seq01_angle_front_*' grouped together)
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
[ Train: 70% ] [ Val: 20% ] [ Test: 10% ]
      │            │            │
      └────────────┼────────────┘
                   │
                   ▼
    [ Cross-Split Leakage Auditor ]
    - Exact SHA-256 Collision Check
    - Perceptual dHash Near-Duplicate Check
    - Filename Collision Check
```

---

## 2. Leakage Prevention Protocol

Data leakage between training and testing sets is a primary failure mode in computer vision assessments. Two temporal frames taken fractions of a second apart can look superficially distinct but share identical background features.

### Anti-Leakage Measures Implemented:
1. **Burst & Sequence Grouping:** The script `dataset/split_dataset.py` extracts capture burst prefixes (e.g. `seq01_*`, `capture_1731_*`). All images from the same camera sweep or lighting session are allocated as an indivisible unit into either Train, Val, or Test.
2. **SHA-256 Cryptographic Hash Check:** Identifies bitwise identical images across splits.
3. **Perceptual Difference Hash (`dHash`):** Computes a 64-bit gradient hash of every image. Any pair across splits with Hamming distance $\le 2$ is flagged as a near-duplicate violation.
4. **Untouched Test Set:** The test partition is reserved strictly for final milestone evaluation and is never seen during hyperparameter optimization or training iterations.

---

## 3. Split Distribution Evidence

Visual representation of the partitioning policy:
- **Evidence Chart:** `05_correct_split/split_distribution.png`
- **Audit Verification Output:** `05_correct_split/leakage_verification.txt`
- **JSON Metadata:** `05_correct_split/leakage_report.json`

---

## 4. Execution Commands

```powershell
# Execute official 70/20/10 sequence-aware split
python dataset/split_dataset.py

# Execute automated cross-split leakage audit
python dataset/check_leakage.py
```
