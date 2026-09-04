import json

from app.pipeline import process_document


IMAGE_PATH = "data/input/test_mcq.png"
OUTPUT_PATH = "data/output/test_mcq.json"


def main():

    print("===================================")
    print("       MCQ JSON GENERATOR")
    print("===================================")

    print("\nProcessing document...")

    result = process_document(
        IMAGE_PATH,
        OUTPUT_PATH
    )

    print(
        f"\nQuestions detected: "
        f"{len(result['questions'])}"
    )

    print(
        f"Layout: "
        f"{result['document']['layout']}"
    )

    print(
        f"\nJSON saved to:\n"
        f"{OUTPUT_PATH}"
    )

    print("\n===== QUESTIONS =====")

    for question in result["questions"]:

        print(
            f"\nQ{question['question_number']}: "
            f"{question['question']}"
        )

        for option in question["options"]:

            print(
                f"  {option['label']}. "
                f"{option['text']}"
            )


if __name__ == "__main__":
    main()