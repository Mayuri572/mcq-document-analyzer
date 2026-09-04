from pathlib import Path
import time

from PIL import Image

from ocr_engine import extract_ocr
from layout_detector import detect_columns
from line_builder import build_lines
from mcq_parser import parse_questions
from json_exporter import save_json


def words_to_text(words: list[dict]) -> str:
    """
    Convert OCR words into readable text using the
    line information produced by Tesseract.
    """

    lines = build_lines(words)

    return "\n".join(
        line["text"]
        for line in lines
        if line["text"].strip()
    )


def process_image(
    image_path: str | Path,
    output_path: str | Path = "data/output/test_mcq.json"
) -> dict:
    """
    Process a single image and generate structured MCQ JSON.

    Pipeline:
        Image
        -> OCR
        -> Layout Detection
        -> Column Processing
        -> Line Reconstruction
        -> MCQ Extraction
        -> Validation
        -> JSON
    """

    start_time = time.perf_counter()

    image_path = Path(image_path)
    output_path = Path(output_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"File not found: {image_path}"
        )

    # =========================================================
    # 1. Open image
    # =========================================================

    image = Image.open(image_path)

    page_width, page_height = image.size

    print("1. Running OCR...")

    # OCR original image.
    words = extract_ocr(image_path)

    print(
        f"   OCR words detected: {len(words)}"
    )

    # =========================================================
    # 2. Detect layout
    # =========================================================

    print("2. Detecting document layout...")

    layout = detect_columns(words)

    detected_layout = layout.get(
        "layout",
        "single-column"
    )

    print(
        f"   Layout detected: {detected_layout}"
    )

    questions = []
    extracted_sections = []

    # =========================================================
    # 3. Two-column document
    # =========================================================

    if detected_layout == "two-column":

        split_x = layout.get("split_x")

        # Fallback if detector does not provide split_x.
        if split_x is None:
            split_x = page_width // 2

        split_x = int(split_x)

        # IMPORTANT:
        # split_x must belong to the ORIGINAL image.
        # Never allow it outside the original image bounds.
        split_x = max(
            1,
            min(
                split_x,
                page_width - 1
            )
        )

        print(
            f"   Column split: x={split_x}"
        )

        # -----------------------------------------------------
        # Crop left and right columns
        # -----------------------------------------------------

        left_image = image.crop(
            (
                0,
                0,
                split_x,
                page_height
            )
        )

        right_image = image.crop(
            (
                split_x,
                0,
                page_width,
                page_height
            )
        )

        left_path = (
            image_path.parent /
            "_left_column_temp.png"
        )

        right_path = (
            image_path.parent /
            "_right_column_temp.png"
        )

        left_image.save(left_path)
        right_image.save(right_path)

        try:

            # =================================================
            # LEFT COLUMN
            # =================================================

            print("3. Processing left column...")

            left_words = extract_ocr(
                left_path
            )

            left_text = words_to_text(
                left_words
            )

            extracted_sections.append(
                {
                    "column": 1,
                    "text": left_text
                }
            )

            left_questions = parse_questions(
                left_text,
                page=1,
                column=1
            )

            # =================================================
            # RIGHT COLUMN
            # =================================================

            print("4. Processing right column...")

            right_words = extract_ocr(
                right_path
            )

            right_text = words_to_text(
                right_words
            )

            extracted_sections.append(
                {
                    "column": 2,
                    "text": right_text
                }
            )

            right_questions = parse_questions(
                right_text,
                page=1,
                column=2
            )

            # Combine both columns.
            questions.extend(
                left_questions
            )

            questions.extend(
                right_questions
            )

        finally:

            # Always remove temporary files.
            left_path.unlink(
                missing_ok=True
            )

            right_path.unlink(
                missing_ok=True
            )

    # =========================================================
    # 4. Single-column document
    # =========================================================

    else:

        print("3. Processing single column...")

        page_text = words_to_text(
            words
        )

        extracted_sections.append(
            {
                "column": 1,
                "text": page_text
            }
        )

        questions = parse_questions(
            page_text,
            page=1,
            column=1
        )

    # =========================================================
    # 5. Sort questions by question number
    # =========================================================

    questions.sort(
        key=lambda question: (
            question.get(
                "question_number",
                999999
            ),
            question.get(
                "page",
                999999
            )
        )
    )

    # =========================================================
    # 6. Remove duplicate question numbers
    # =========================================================

    unique_questions = []
    seen_numbers = set()

    for question in questions:

        number = question.get(
            "question_number"
        )

        # Keep questions without a number.
        if number is None:
            unique_questions.append(
                question
            )
            continue

        # Remove duplicate numbered questions.
        if number in seen_numbers:

            print(
                f"   Warning: duplicate question "
                f"number ignored: {number}"
            )

            continue

        seen_numbers.add(number)

        unique_questions.append(
            question
        )

    questions = unique_questions

    # =========================================================
    # 7. Validate extracted options
    # =========================================================

    complete_questions = 0
    questions_needing_review = 0
    total_options = 0

    expected_labels = [
        "A",
        "B",
        "C",
        "D"
    ]

    for question in questions:

        options = question.get(
            "options",
            []
        )

        total_options += len(options)

        labels = [
            option.get(
                "label",
                ""
            ).upper()
            for option in options
        ]

        missing_options = [
            label
            for label in expected_labels
            if label not in labels
        ]

        complete = (
            len(options) == 4
            and labels == expected_labels
        )

        question["validation"] = {
            "options_detected": len(options),
            "options_expected": 4,
            "missing_options": missing_options,
            "complete": complete,
            "needs_review": not complete
        }

        if complete:
            complete_questions += 1
        else:
            questions_needing_review += 1

    # =========================================================
    # 8. Combine actual OCR text
    # =========================================================

    extracted_text = "\n\n".join(
        (
            f"===== COLUMN {section['column']} =====\n"
            f"{section['text']}"
        )
        for section in extracted_sections
    )

    # =========================================================
    # 9. Processing time
    # =========================================================

    processing_time = (
        time.perf_counter() - start_time
    )

    # =========================================================
    # 10. Create final result
    # =========================================================

    result = {

        "document": {
            "file_name": image_path.name,
            "file_type": (
                image_path.suffix
                .lower()
                .replace(".", "")
            ),
            "page_count": 1,
            "language": "en",
            "layout": detected_layout
        },

        "processing": {
            "status": "completed",
            "ocr_engine": "Tesseract",
            "processing_time_seconds": round(
                processing_time,
                2
            ),
            "ocr_word_count": len(words)
        },

        "extraction_summary": {
            "questions_detected": len(questions),
            "complete_questions": complete_questions,
            "questions_needing_review": questions_needing_review,
            "total_options_detected": total_options,
            "expected_options": len(questions) * 4
        },

        # REAL text extracted from the uploaded image.
        "extracted_text": extracted_text,

        # Structured MCQ data.
        "questions": questions
    }

    # =========================================================
    # 11. Save REAL JSON file
    # =========================================================

    save_json(
        result,
        output_path
    )

    print(
        f"6. JSON saved to: {output_path}"
    )

    return result