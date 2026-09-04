from pathlib import Path
import pytesseract
from PIL import Image


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
IMAGE_PATH = Path("data/input/test_mcq.png")


def main():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    if not IMAGE_PATH.exists():
        print(f"ERROR: Image not found: {IMAGE_PATH}")
        return

    image = Image.open(IMAGE_PATH)

    print("Processing image...")
    print(f"Image size: {image.size}")

    # OCR text
    text = pytesseract.image_to_string(image, lang="eng")

    print("\n========== OCR TEXT ==========\n")
    print(text)

    # OCR with bounding boxes
    data = pytesseract.image_to_data(
        image,
        lang="eng",
        output_type=pytesseract.Output.DICT
    )

    print("\n========== OCR BOXES ==========\n")

    count = 0

    for i, word in enumerate(data["text"]):
        word = word.strip()

        if word:
            print(
                f"text={word!r} | "
                f"x={data['left'][i]} | "
                f"y={data['top'][i]} | "
                f"w={data['width'][i]} | "
                f"h={data['height'][i]} | "
                f"confidence={data['conf'][i]}"
            )
            count += 1

    print(f"\nDetected words: {count}")


if __name__ == "__main__":
    main()