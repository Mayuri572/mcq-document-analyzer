from app.ocr_engine import extract_ocr
from app.layout_detector import detect_columns


IMAGE_PATH = "data/input/test_mcq.png"


def main():
    print("Running OCR...")

    words = extract_ocr(IMAGE_PATH)

    print(f"Detected words: {len(words)}")

    print("\nDetecting layout...")

    result = detect_columns(words)

    print(f"\nLayout: {result['layout']}")

    for column in result["columns"]:
        print(
            f"\nColumn {column['column']}: "
            f"{len(column['words'])} words"
        )

        preview = column["words"][:15]

        for word in preview:
            print(
                f"{word['text']} "
                f"(x={word['x']}, y={word['y']})"
            )


if __name__ == "__main__":
    main()