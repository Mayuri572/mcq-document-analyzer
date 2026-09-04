from app.pipeline import process_document


IMAGE_PATH = "data/input/test_mcq.png"


def main():
    print("===================================")
    print("     MCQ DOCUMENT ANALYZER")
    print("===================================")

    print("\nProcessing document...")

    result = process_document(IMAGE_PATH)

    print("\nDocument:")
    print(result["document"])

    print("\nOCR:")
    print(result["ocr"])

    print("\nLayout:")
    print(result["layout"])

    print("\nColumns:")
    for column in result["columns"]:
        print(
            f"Column {column['column']}: "
            f"{len(column['words'])} words"
        )

    print("\nProcessing complete.")


if __name__ == "__main__":
    main()