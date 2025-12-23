import cv2
import sys
from pathlib import Path

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