import cv2

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
