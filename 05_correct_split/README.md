# Deliverable 5: Correct Dataset Split & Leakage Verification Dossier

**Milestone:** M1 (DETECT)  
**Deliverable ID:** D5 – Correct Split  
**Target Ratios:** 70% Training / 20% Validation / 10% Testing  
**Auditor Engine:** `dataset/check_leakage.py`  
**Date:** November 10, 2026

---

## 1. Verified Evidence Files in this Folder

| File Name | Description | Verification Method |
| :--- | :--- | :--- |
| `split_distribution.png` | Visual pie chart illustrating 70/20/10 target partition | Generated via `dataset/split_dataset.py` |
| `leakage_verification.txt` | Human-readable audit report logging collisions and violations | Generated via `dataset/check_leakage.py` |
| `leakage_report.json` | Programmatic verification log with SHA-256 and dHash records | Generated via `dataset/check_leakage.py` |
| `split_summary.json` | Partition statistics, exact counts, percentages, and seed | Generated via `dataset/split_dataset.py` |

---

## 2. Leakage Verification Criteria

- [x] Zero filename overlap across partitions
- [x] Zero cryptographic SHA-256 cross-split collisions
- [x] Zero perceptual near-duplicate cross-split leaks (Hamming distance $\le 2$)
- [x] Sequence burst preservation enforced
- [x] Untouched test set policy established

---

## 3. Reproduction Command
```powershell
python dataset/split_dataset.py
python dataset/check_leakage.py
```
