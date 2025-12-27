import cv2
import sys
from pathlib import Path
import pytesseract
import re

def load_image(image_path: str):
    """
    Loads an image from disk using OpenCV.

    OpenCV loads images in BGR format by default
    (not RGB, this matters later).
    """
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not load image at {image_path}")

    return image

def resize_image(image, max_width=1800):
    """
    Resizes image while maintaining aspect ratio.
    Improves OCR performance on phone images.
    """
    h, w = image.shape[:2]

    if w <= max_width:
        return image

    scale = max_width / w
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized



def to_grayscale(image):
    """
    Converts a BGR image to grayscale.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def denoise(gray_image):
    """
    Applies Gaussian Blur to reduce noise.
    """
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    return blurred

def apply_threshold(blurred_image):
    """
    Converts a grayscale blurred image into
    a black-and-white (binary) image using
    adaptive thresholding.
    """
    thresh = cv2.adaptiveThreshold(
        blurred_image,
        255,  # max value for white
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,   # size of local neighborhood
        4     # constant subtracted from mean
    )
    return thresh

def apply_morphology(binary_image):
    """
    Applies morphological closing to strengthen
    text strokes and close small gaps.
    """
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    processed = cv2.morphologyEx(
        binary_image,
        cv2.MORPH_CLOSE,
        kernel
    )
    return processed

# OCR function
def run_ocr(image):
    """
    Runs Tesseract OCR on a preprocessed image
    and returns raw OCR data including bounding boxes.
    """
    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )
    return data

def is_price(text):
    return bool(re.match(r"^[₹$]?\d+(\.\d{2})?$", text))

def is_valid_word(text):
    """
    Filters out OCR junk like random symbols.
    """
    if len(text) == 1 and not text.isalnum():
        return False

    # Reject words with too many special chars
    if len(re.findall(r"[^\w\d]", text)) > 2:
        return False

    return True

def is_total_line(text):
    keywords = ["total", "amount", "grand"]
    t = text.lower()
    return any(k in t for k in keywords)


def extract_words(ocr_data, min_conf=0):
    """
    Converts raw Tesseract OCR output into
    a list of word objects, filtering low-confidence noise.
    """
    words = []

    n = len(ocr_data["text"])

    for i in range(n):
        text = ocr_data["text"][i].strip()
        conf = int(ocr_data["conf"][i])

        if text == "" or conf < min_conf:
            continue
        if not is_valid_word(text):
            continue

        word = {
            "text": text,
            "x": ocr_data["left"][i],
            "y": ocr_data["top"][i],
            "w": ocr_data["width"][i],
            "h": ocr_data["height"][i],
            "conf": conf
        }
        words.append(word)

    return words

def group_words_into_lines(words, y_threshold=20):
    """
    Groups words into lines based on vertical proximity.
    """
    lines = []

    for word in words:
        placed = False

        for line in lines:
            if abs(word["y"] - line["y"]) < y_threshold:
                line["words"].append(word)
                placed = True
                break

        if not placed:
            lines.append({
                "y": word["y"],
                "words": [word]
            })

    # Sort words inside each line by X coordinate
    for line in lines:
        line["words"].sort(key=lambda w: w["x"])

    # Sort lines top to bottom
    lines.sort(key=lambda l: l["y"])

    return lines

def lines_to_text(lines):
    result = []

    for line in lines:
        words = line["words"]
        text = " ".join(w["text"] for w in words)

        # Boost confidence if line contains a price
        if any(is_price(w["text"]) for w in words):
            result.append(text)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <image_path>")
        sys.exit(1)

# Step1: Load the image
    image_path = sys.argv[1]
    img = load_image(image_path)
    img = resize_image(img)

    print("Image shape:", img.shape)
    print("Image dtype:", img.dtype)

# Step 2: Convert to grayscale
    gray = to_grayscale(img)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    cv2.imwrite(str(output_dir / "gray.jpg"), gray)
    print("Saved grayscale image")

# Step 3: Apply Gaussian blur
    blurred = denoise(gray)
    cv2.imwrite(str(output_dir / "blurred.jpg"), blurred)
    print("Saved blurred image")

# Step 4: Apply adaptive thresholding
    thresh = apply_threshold(blurred)
    cv2.imwrite(str(output_dir / "threshold.jpg"), thresh)
    print("Saved thresholded image")

# Step 5: Apply morphological operations
    final = apply_morphology(thresh)
    cv2.imwrite(str(output_dir / "final.jpg"), final)
    print("Saved final OCR-ready image")

# Step 6: Run OCR
    ocr_data = run_ocr(final)

# Save raw OCR output for inspection
import json
with open("outputs/ocr_raw.json", "w") as f:
    json.dump(ocr_data, f, indent=2)

print("Saved raw OCR data")

# Step 7: Extract words
words = extract_words(ocr_data)
lines = group_words_into_lines(words)
line_texts = lines_to_text(lines)

# Save readable lines for inspection
with open("outputs/lines.txt", "w") as f:
    for line in line_texts:
        f.write(line + "\n")

print("Saved grouped OCR lines")
