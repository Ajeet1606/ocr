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
Noise removal (Gaussian Blur)
   ↓
Adaptive Threshold
   ↓
Morphological Closing
   ↓
OCR-ready Image
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

## 7️⃣ Thresholding & Morphology

### 🎯 Goal

Prepare an image so that OCR can reliably distinguish text from background, even under:

- uneven lighting
- shadows
- camera noise
- handwritten strokes

### 7.1 Thresholding

#### 🔹 What is Thresholding?

Thresholding converts a grayscale image into a binary image:

- **Black** → text
- **White** → background

This simplifies the image so OCR engines can focus only on character shapes.

#### 🔹 Why Grayscale Is Not Enough

Grayscale images still contain:

- shadows
- lighting gradients
- background texture

OCR engines struggle to decide:

> “Is this pixel text or background?”

Thresholding answers that question.

### 7.2 Types of Thresholding

#### ❌ Global Thresholding

Rule:

```
if pixel_value > X → white
else → black
```

#### Problems:

- fails with uneven lighting
- breaks on phone images
- sensitive to shadows
- Used only in controlled environments.

#### ✅ Adaptive Thresholding (Recommended)

Rule:

> threshold is computed locally for each region

Each pixel is compared against the local mean of its neighborhood.

**Advantages:**

- handles shadows
- handles paper color variation
- works well for invoices and handwritten notes

```
cv2.adaptiveThreshold(
    image,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    blockSize,
    C
)
```

#### 🔹 Important Parameters

`blockSize`

- Size of the local neighborhood
- Must be an odd number
- Smaller → more sensitive
- Larger → smoother result

Typical values: 11, 15

`C`

- Constant subtracted from the local mean
- Controls text thickness

Effects:

- Higher C → thinner text
- Lower C → bolder text

#### 🔹 Output Characteristics

A good thresholded image has:

- white background
- solid black text
- minimal noise
- clear character separation

### 7.4 Morphological Operations

#### 🔹 Why Morphology Is Needed

Thresholding can cause:

- broken characters
- thin strokes
- small gaps in handwriting

Morphology helps repair and strengthen text.

### 7.5 Key Morphological Operations

| Operation | Effect              |
| --------- | ------------------- |
| Dilation  | Thickens text       |
| Erosion   | Thins text          |
| Opening   | Removes small noise |
| Closing   | Fills small gaps    |

For OCR, Closing is the most useful.

### 7.6 Morphological Closing

**Closing = Dilation → Erosion**

This:

- connects broken strokes
- fills small holes
- strengthens characters

```
kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (2, 2)
)

processed = cv2.morphologyEx(
    binary_image,
    cv2.MORPH_CLOSE,
    kernel
)
```

#### 🔹 Kernel Size

- Small kernel (2,2) → subtle fixing
- Large kernel → text may merge or blur

Kernel choice is image-dependent.

### 7.8 Final OCR-Ready Image

After thresholding + morphology, the image:

- may look ugly to humans
- but is ideal for OCR

OCR prefers clarity over beauty.

### 🧠 Key Takeaways

- OCR success depends more on CV preprocessing than OCR models
- Adaptive thresholding handles real-world images best
- Morphology repairs thresholding artifacts
- Always visually inspect intermediate outputs
