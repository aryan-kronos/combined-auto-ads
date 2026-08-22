# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import re


def parse_interval(text: str):

    text = text.strip().lower()

    match = re.fullmatch(
        r"(\d+)(m|h|d)",
        text
    )

    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if unit == "m":
        seconds = value * 60

    elif unit == "h":
        seconds = value * 3600

    else:
        seconds = value * 86400

    # Minimum 5 minutes
    if seconds < 300:
        return None

    # Maximum 30 days
    if seconds > 2592000:
        return None

    return seconds