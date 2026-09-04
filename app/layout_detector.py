def detect_columns(words: list[dict]) -> dict:
    """
    Detect whether the document body uses one or two columns.

    Strategy:
    - Ignore the header region.
    - Find the horizontal extent of the document body.
    - Use the midpoint of that extent as the candidate column split.
    - Check whether both sides contain substantial content.
    """

    if not words:
        return {
            "layout": "unknown",
            "columns": []
        }

    # Ignore heading/header area.
    body_words = [
        word
        for word in words
        if word["y"] >= 80
    ]

    if len(body_words) < 10:
        return {
            "layout": "single-column",
            "split_x": None,
            "columns": [
                {
                    "column": 1,
                    "words": sorted(
                        body_words,
                        key=lambda w: (w["y"], w["x"])
                    )
                }
            ]
        }

    # Find the horizontal extent of the body content.
    min_x = min(
        word["x"]
        for word in body_words
    )

    max_x = max(
        word["x"] + word["width"]
        for word in body_words
    )

    # Candidate center of body content.
    split_x = (min_x + max_x) / 2

    left_words = []
    right_words = []

    for word in body_words:

        center_x = (
            word["x"] +
            word["width"] / 2
        )

        if center_x < split_x:
            left_words.append(word)
        else:
            right_words.append(word)

    # Sort each column top-to-bottom,
    # then left-to-right.
    left_words.sort(
        key=lambda w: (w["y"], w["x"])
    )

    right_words.sort(
        key=lambda w: (w["y"], w["x"])
    )

    total = (
        len(left_words) +
        len(right_words)
    )

    # Require meaningful content on both sides.
    if (
        total > 0
        and len(left_words) / total >= 0.25
        and len(right_words) / total >= 0.25
    ):

        return {
            "layout": "two-column",

            # IMPORTANT:
            # This is the detected split position.
            "split_x": round(
                split_x,
                2
            ),

            "columns": [
                {
                    "column": 1,
                    "words": left_words
                },
                {
                    "column": 2,
                    "words": right_words
                }
            ]
        }

    # Otherwise treat as single column.
    return {
        "layout": "single-column",
        "split_x": None,
        "columns": [
            {
                "column": 1,
                "words": body_words
            }
        ]
    }