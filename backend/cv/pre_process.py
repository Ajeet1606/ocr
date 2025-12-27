import cv2

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
