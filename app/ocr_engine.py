from pathlib import Path

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def prepare_image(image):
    """Prepare image for OCR."""

    # Upscale
    image = image.resize(
        (image.width * 2, image.height * 2)
    )

    # Grayscale
    image = image.convert("L")

    # Contrast
    image = ImageEnhance.Contrast(image).enhance(1.5)

    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)

    return image


def extract_ocr(image_path: str | Path) -> list[dict]:

    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = Image.open(image_path)

    image = prepare_image(image)

    data = pytesseract.image_to_data(
        image,
        lang="eng",
        output_type=pytesseract.Output.DICT,
        config="--psm 3"
    )

    words = []

    for i, text in enumerate(data["text"]):

        text = text.strip()

        if not text:
            continue

        try:
            confidence = float(data["conf"][i])
        except:
            confidence = 0.0

        words.append(
            {
                "text": text,
                "x": int(data["left"][i]),
                "y": int(data["top"][i]),
                "width": int(data["width"][i]),
                "height": int(data["height"][i]),
                "confidence": confidence,

                # IMPORTANT
                "block_num": data["block_num"][i],
                "par_num": data["par_num"][i],
                "line_num": data["line_num"][i],
                "word_num": data["word_num"][i],
            }
        )

    return words