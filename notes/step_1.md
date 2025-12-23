## Image Preparation for OCR:

Prepare an image so that OCR can read it reliably.

Key idea:

OCR accuracy depends more on image quality than on the OCR model itself.

### 🧠 Big Picture Pipeline

```
Raw Image
   ↓
Load image (BGR)
   ↓
Grayscale
   ↓
Noise removal
   ↓
(OCR-ready image)
```

We’re still in Computer Vision (CV) territory — no OCR, no AI yet.

## 1️⃣ Python as a Tool (Not a Goal)

### Why Python?

- Strong CV ecosystem
- Less boilerplate
- Fast experimentation

### What we used

- Functions
- CLI arguments
- File paths
- Basic modules

We are not learning Python deeply, just enough to control CV.

## 2️⃣ How Computers See Images

### Core concept

An image is a matrix of numbers.

```
Height × Width × Channels
```

- Color image → (H, W, 3)
- Grayscale → (H, W)
- Data type → uint8 (0–255)

#### OCR prefers:

- fewer channels
- high contrast
- low noise

## 3️⃣ Image Loading

### What we did

```
cv2.imread(path)
```

### Why it matters:

- OpenCV loads images in BGR, not RGB
- Understanding format prevents bugs later

#### We verified:

- shape
- data type

## 4️⃣ Grayscale Conversion

### Why grayscale?

- OCR doesn’t care about color
- Shadows & color gradients confuse OCR
- Reduces complexity

### Operation

```
cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

#### Result

- Image becomes a single-channel intensity map
- Text becomes clearer

## 5️⃣ Noise Removal (Gaussian Blur)

### What is noise?

- Random pixel variations
- Camera artifacts
- Paper texture

### Why remove noise?

- OCR mistakes noise as characters
- Breaks character boundaries

### Operation

```
cv2.GaussianBlur(gray, (5, 5), 0)
```

### Trade-off

- Slightly softer edges
- Much better OCR reliability

## 6️⃣ Saving Intermediate Outputs (Very Important)

### Why we save each step

- CV is visual debugging
- You must see transformations
- Makes failures obvious

#### Saved outputs:

- gray.jpg
- blurred.jpg
- This habit is critical in real CV systems.

## 🧠 Key Mental Models You Learned

1. OCR is downstream

   - If CV is bad, OCR cannot fix it

2. CV is deterministic

   - Same input → same output
   - Debuggable visually

3. Don’t treat images as black boxes
   - Inspect shapes, values, and outputs
