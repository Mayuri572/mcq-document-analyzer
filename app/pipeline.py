from pathlib import Path

from app.ocr_engine import extract_ocr
from app.line_builder import build_lines
from app.layout_detector import detect_columns


def process_document(
    image_path: str | Path
):

    image_path = Path(image_path)

    # 1. OCR
    words = extract_ocr(image_path)

    # 2. Reconstruct OCR lines
    lines = build_lines(words)

    # 3. Detect document layout
    layout = detect_columns(words)

    return {
        "document": {
            "file_name": image_path.name,
            "file_type": image_path.suffix.lower().replace(".", ""),
            "page_count": 1,
            "language": "en",
            "layout": layout["layout"]
        },

        "processing": {
            "ocr_engine": "Tesseract",
            "status": "completed",
            "word_count": len(words),
            "line_count": len(lines)
        },

        "ocr": {
            "words": words,
            "lines": lines
        }
    }   