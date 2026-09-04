import re


QUESTION_PATTERN = re.compile(
    r"^\s*(?:Q(?:uestion)?\s*)?(\d{1,3})\s*[\.\):\-]?\s*$",
    re.IGNORECASE,
)


def is_question_start(text: str) -> bool:
    """
    Return True when OCR text looks like a question number.
    Examples:
        1.
        7.
        10.
        Q1
        Q10.
        Question 12
    """
    text = text.strip()

    # Remove common OCR noise before checking.
    cleaned = text.replace("ô", "").replace("O", "")

    return bool(QUESTION_PATTERN.match(cleaned))


def extract_question_number(text: str):
    """
    Extract the question number if the text represents one.
    """
    text = text.strip()

    cleaned = (
        text.replace("ô", "")
        .replace("O", "")
        .replace("Q.", "Q")
    )

    match = re.search(r"(\d{1,3})", cleaned)

    if match:
        return int(match.group(1))

    return None