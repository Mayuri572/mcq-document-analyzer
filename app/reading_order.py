def sort_words_by_reading_order(words: list[dict]) -> list[dict]:
    """
    Sort OCR words from top to bottom and left to right.
    """

    return sorted(
        words,
        key=lambda word: (
            word["y"],
            word["x"]
        )
    )


def sort_columns(columns: list[dict]) -> list[dict]:
    """
    Sort columns from left to right.
    """

    return sorted(
        columns,
        key=lambda column: min(
            word["x"] for word in column["words"]
        )
    )