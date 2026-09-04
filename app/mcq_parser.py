import re


QUESTION_PATTERN = re.compile(
    r"^\s*(?:question\s*)?(\d{1,3})\s*[\.\):\-]\s*(.*)$",
    re.IGNORECASE
)

OPTION_PATTERN = re.compile(
    r"^\s*[\(\[]?([A-Da-d])[\)\].:\-]\s*(.*)$"
)


def normalize_text(text: str) -> str:
    """Clean common OCR artifacts while preserving useful text."""

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "æ": "",
        "⌐": "",
        "ô": "",
        "Â": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def parse_questions(text: str, page: int = 1, column: int = 1):
    """
    Convert OCR text into structured MCQs.
    """

    lines = [
        normalize_text(line)
        for line in text.splitlines()
    ]

    lines = [line for line in lines if line]

    questions = []
    current = None
    current_option = None

    for line in lines:

        # Check for question start.
        question_match = QUESTION_PATTERN.match(line)

        if question_match:
            if current:
                questions.append(current)

            number = int(question_match.group(1))
            question_text = question_match.group(2).strip()

            current = {
                "question_number": number,
                "question": question_text,
                "options": [],
                "page": page,
                "column": column
            }

            current_option = None
            continue

        # Check for A/B/C/D option.
        option_match = OPTION_PATTERN.match(line)

        if option_match and current:
            option_label = option_match.group(1).upper()
            option_text = option_match.group(2).strip()

            current["options"].append({
                "label": option_label,
                "text": option_text
            })

            current_option = current["options"][-1]
            continue

        # Continuation of question or option text.
        if current:

            if current_option:
                current_option["text"] += " " + line
            else:
                current["question"] += " " + line

    if current:
        questions.append(current)

    return questions