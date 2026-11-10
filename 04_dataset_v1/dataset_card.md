# Dataset Card: Rhino Motion RMCS-610 Enclosure Detection (Dataset V1)

**Dataset Name:** `rmcs610-enclosure-v1`  
**Object Class:** Single Class — `0: enclosure`  
**Domain:** Industrial Edge AI & Automated Optical Inspection (AOI)  
**Version:** 1.0.0-pending  
**Author:** Edge AI Computer Vision Team  
**Date:** November 10, 2026  

---

## 1. Dataset Purpose & Description
The `rmcs610-enclosure-v1` dataset is designed to train lightweight object detection models (such as YOLOv8n / YOLOv11n) to detect the assembled housing of the **Rhino Motion RMCS-610 Digital Speed Controller**.

### Target Object Definition
- **Class ID:** `0`
- **Class Name:** `enclosure`
- **Physical Composition:** The upper lid (`top` in CAD) and base chassis (`bottom` in CAD) mounted together as **ONE single assembled unit**.
- **Internal Components Exclusion:** The internal PCB, terminals, power semiconductors, and potentiometer (`component` in CAD) are internal structures and are strictly **excluded** from independent bounding box annotation.

---

## 2. Photographic Collection Methodology

In strict compliance with assignment guidelines:
- **No CAD Renders:** Synthetic CAD renderings or virtual screenshots are strictly prohibited from the training dataset.
- **Physical Sensor:** Captured using real device cameras under genuine physical illumination.
- **Perspective Coverage Matrix:**
  1. **Primary Views:** Front elevation, Rear elevation, Left profile, Right profile, Top plan view.
  2. **Oblique Perspectives:** Isometric angular captures ($15^\circ, 30^\circ, 45^\circ, 60^\circ$).
  3. **Operational Distances:** Close-up inspection ($15\text{–}30\text{ cm}$), medium workbench distance ($40\text{–}80\text{ cm}$), wide field ($1\text{–}1.5\text{ m}$).
  4. **Lighting Conditions:** High ambient daylight, fluorescent overhead laboratory lighting, oblique shadow lighting, low-light underexposed conditions.
  5. **Background Variability:** Industrial workbench, anti-static mat, metallic table, cluttered electronics desk.

---

## 3. Annotation Specification

- **Annotation Format:** Standard YOLO Normalized Bounding Boxes:
  $$\text{class\_id}\quad x_{\text{center}}\quad y_{\text{center}}\quad \text{width}\quad \text{height}$$
  where:
  - $\text{class\_id} = 0$
  - $0.0 \le x_{\text{center}}, y_{\text{center}}, \text{width}, \text{height} \le 1.0$
- **Bounding Box Tightness:** Tight bounding box encompassing the external boundary contours of the assembled chassis without excessive background padding.
- **Occlusion Policy:** If the enclosure is partially occluded ($< 50\%$), annotate the visible envelope. If occluded $\ge 50\%$, omit or flag as truncated.

---

## 4. Quality Control & Automated Verification

Automated validation is executed via `dataset/validate_dataset.py`:
1. **Coordinate Boundary Audit:** Verifies $0.0 \le x, y, w, h \le 1.0$.
2. **Degenerate Geometry Check:** Fails any box with $w \le 0$ or $h \le 0$.
3. **Class ID Integrity:** Asserts that only integer `0` is present.
4. **Duplicate Deduplication:** Calculates SHA-256 and perceptual 64-bit difference hashes (`dHash`) to prevent duplicated frames from contaminating splits.
5. **Missing Label Verification:** Enforces a 1:1 image-to-label parity.

---

## 5. Current Dataset State & Physical Tasks

> [!IMPORTANT]
> **Status: PENDING PHYSICAL IMAGE ACQUISITION**  
> The annotation infrastructure, schema, and automated verification tools are fully implemented and verified. The user must capture photographs of their physical RMCS-610 controller using `camera/camera_capture.py` or a mobile device, place them into `dataset/images/`, and execute `python dataset/annotate_dataset.py`.
