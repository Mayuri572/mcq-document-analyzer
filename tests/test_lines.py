from app.ocr_engine import extract_ocr
from app.line_builder import build_lines


IMAGE_PATH = "data/input/test_mcq.png"


def main():

    print("Running OCR...")

    words = extract_ocr(IMAGE_PATH)

    lines = build_lines(words)

    print(f"Words detected: {len(words)}")
    print(f"Lines detected: {len(lines)}")

    print("\n========== RECONSTRUCTED LINES ==========\n")

    for line in lines:

        print(
            f"y={line['y']:4} "
            f"x={line['x']:4} "
            f"| {line['text']}"
        )


if __name__ == "__main__":
    main()