import cv2
import sys
from pathlib import Path
import pytesseract

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
        11,   # size of local neighborhood
        2     # constant subtracted from mean
    )
    return thresh

def apply_morphology(binary_image):
    """
    Applies morphological closing to strengthen
    text strokes and close small gaps.
    """
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (2, 2)
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <image_path>")
        sys.exit(1)

# Step1: Load the image
    image_path = sys.argv[1]
    img = load_image(image_path)

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
