import sys
import cv2
import json
from pathlib import Path

from cv.load_image import load_image, resize_image
from cv.pre_process import to_grayscale, denoise, apply_threshold, apply_morphology
from ocr.tesseract import run_ocr
from structure.lines import extract_words, group_words_into_lines, lines_to_text
from structure.invoice import build_invoice_sections
from format.markdown import generate_markdown
from llm.qa import load_markdown, build_prompt, ask_llm

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <image_path>")
        sys.exit(1)

# Step 1: Load the image
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

    header, items, totals = build_invoice_sections(line_texts)
    markdown = generate_markdown(header, items, totals)

    with open("outputs/document.md", "w") as f:
        f.write(markdown)

    print("Generated Markdown invoice")

    question = input("\nAsk a question about the invoice: ")

    document = load_markdown()
    prompt = build_prompt(document, question)
    answer = ask_llm(prompt)

    print("\nAnswer:\n", answer)
