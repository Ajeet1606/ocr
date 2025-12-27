# 📘 Day-2 Notes — OCR → Structure (Invoices)

## 🎯 Objective

Convert a real-world invoice image into structured, readable text using:

- **Computer vision**
- **OCR**
- **Geometry-based logic**

> The goal is useful understanding, not perfect OCR.

---

## 🧠 Big Picture Pipelines

```
1. OCR-ready Image (Day-1)
  ↓
2. OCR Engine (Tesseract)
  ↓
3. Words + Bounding Boxes
  ↓
4. Line Grouping (Geometry)
  ↓
5. Noise Filtering
  ↓
6. Structured Lines
```

---

## 1️⃣ OCR Fundamentals

### What OCR Actually Does

OCR performs:

- Text region segmentation
- Character recognition
- Geometry + confidence reporting

OCR outputs:

- Words (not lines)
- Bounding boxes
- Confidence scores

OCR does **not**:

- Understand invoices
- Group items
- Detect totals

> Structure is the developer’s responsibility.

---

## 2️⃣ Tesseract OCR Integration

### Why Tesseract?

- Open source
- Transparent output
- Imperfect → forces learning
- Industry baseline

#### OCR Output Format

```json
{
  "text": [...],
  "left": [...],
  "top": [...],
  "width": [...],
  "height": [...],
  "conf": [...]
}
```

Each index corresponds to one detected word.

---

## 3️⃣ Bounding Boxes = Spatial Intelligence

Bounding boxes enable:

- Reading order reconstruction
- Line grouping
- Column detection
- Future highlighting of answers

> **Key observation:** Words on the same line have similar Y-coordinates.

---

## 4️⃣ Word Cleaning & Confidence Filtering

### Why Filtering Is Needed

OCR produces:

- Empty tokens
- Punctuation noise
- Low-confidence garbage

**Filtering rules:**

- Ignore empty text
- Ignore low confidence words
- Ignore symbol-heavy tokens

>This improves signal quality dramatically.

---

## 5️⃣ Grouping Words into Lines

### Core Idea

Group words if:

$$
|y_1 - y_2| < \text{threshold}
$$

Then:

- Sort words left → right (**X-axis**)
- Sort lines top → bottom (**Y-axis**)

>This reconstructs how humans read invoices.

---

## 6️⃣ Real-World Invoice Challenges

Phone-clicked invoices introduce:

- Uneven lighting
- Perspective distortion
- Thin fonts
- Thermal paper artifacts

**Fixes applied:**

- Image resizing
- Stronger thresholding
- Larger morphology kernel
- Relaxed line grouping thresholds

> Perfect OCR is not realistic — usefulness is.

---

## 7️⃣ Domain-Specific Heuristics (Invoice Logic)

Invoices are number-centric documents.

**Heuristics added:**

- Detect price-like tokens
- Prioritize lines with currency / numbers
- Detect keywords like total, subtotal, amount

>This is document intelligence, not OCR tuning.

---

## 8️⃣ Results Interpretation

**Observed outcomes:**

- Some text accurate
- Some gibberish
- Line items correctly grouped
- Subtotal detected reliably

>This is expected and acceptable.
>
>**Key insight:**
>
>OCR is probabilistic, structure is deterministic.

---

## 🧠 Key Learnings (Most Important)

- **OCR ≠ understanding**
- **Preprocessing affects OCR more than models**
- **Bounding boxes are more valuable than raw text**
- **Domain heuristics beat OCR perfection**
- **Real systems tolerate noise and reason around it**

---

## 📦 Day-2 Deliverables

```
outputs/
 ├─ ocr_raw.json
 ├─ lines.txt
 └─ (structured invoice lines)
```

You now have:

- Pixels → words → lines
- A usable invoice representation
- A foundation for Markdown + Q&A