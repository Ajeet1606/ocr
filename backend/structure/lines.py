import re

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
