def build_lines(words: list[dict]) -> list[dict]:
    """
    Reconstruct OCR words into natural text lines.
    """

    groups = {}

    for word in words:

        key = (
            word["block_num"],
            word["par_num"],
            word["line_num"]
        )

        groups.setdefault(key, []).append(word)

    lines = []

    for words_in_line in groups.values():

        words_in_line.sort(
            key=lambda word: word["x"]
        )

        text = " ".join(
            word["text"]
            for word in words_in_line
        )

        lines.append(
            {
                "text": text,
                "x": min(
                    word["x"]
                    for word in words_in_line
                ),
                "y": min(
                    word["y"]
                    for word in words_in_line
                ),
                "width": (
                    max(
                        word["x"] + word["width"]
                        for word in words_in_line
                    )
                    -
                    min(
                        word["x"]
                        for word in words_in_line
                    )
                ),
                "height": max(
                    word["height"]
                    for word in words_in_line
                ),
                "words": words_in_line
            }
        )

    lines.sort(
        key=lambda line: (
            line["y"],
            line["x"]
        )
    )

    return lines