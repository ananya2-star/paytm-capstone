import re


def extract_signals(text):

    text_lower = text.lower()

    risk_flags = []

    # Litigation
    if re.search(
        r"\blitigation\b|\blawsuit\b|\blegal\b|\bcourt\b",
        text_lower
    ):
        risk_flags.append("litigation")

    # Regulatory
    if re.search(
        r"\bregulatory\b|\bregulator\b|\bcompliance\b",
        text_lower
    ):
        risk_flags.append("regulatory")

    # Customer concentration
    if re.search(
        r"top\s+three\s+customers|"
        r"customer[s]?\s+account\s+for|"
        r"customer\s+concentration",
        text_lower
    ):
        risk_flags.append("customer_concentration")

    # Hedging / uncertainty
    hedging_detected = bool(
        re.search(
            r"\bassum(?:e|ing)\b|"
            r"\bcautiously\b|"
            r"\bvisibility\b",
            text_lower
        )
    )

    # Sentiment
    if (
        "confident" in text_lower
        or "approved" in text_lower
    ):
        sentiment = "confident"

    elif hedging_detected:
        sentiment = "cautious"

    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment
    }
