import pytesseract

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
