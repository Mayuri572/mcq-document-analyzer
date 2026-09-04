from app.document_processor import process_image


INPUT_FILE = "data/input/test_mcq.png"
OUTPUT_FILE = "data/output/test_mcq.json"


def main():

    print("=" * 50)
    print("       MCQ DOCUMENT ANALYZER")
    print("=" * 50)

    result = process_image(
        INPUT_FILE,
        OUTPUT_FILE
    )

    print("\n========== EXTRACTION RESULT ==========")

    print(
        f"Layout: "
        f"{result['document']['layout']}"
    )

    print(
        f"Questions detected: "
        f"{result['extraction_summary']['questions_detected']}"
    )

    print(
        f"Questions with 4 options: "
        f"{result['extraction_summary']['questions_with_4_options']}"
    )

    print(
        f"Total options detected: "
        f"{result['extraction_summary']['total_options_detected']}"
    )

    print(
        f"\nJSON created at: "
        f"{OUTPUT_FILE}"
    )

    print("\n========== QUESTIONS ==========")

    for q in result["questions"]:

        print(
            f"\nQ{q['question_number']}: "
            f"{q['question']}"
        )

        for option in q["options"]:

            print(
                f"  {option['label']}. "
                f"{option['text']}"
            )

        print(
            f"  Options: "
            f"{q['validation']['options_detected']}/4"
        )


if __name__ == "__main__":
    main()