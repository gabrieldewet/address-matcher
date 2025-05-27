import re
from typing import Optional


def normalize_string(text: Optional[str]) -> Optional[str]:
    """
    Normalizes a string for comparison.
    Converts to lowercase, strips whitespace, and collapses multiple spaces.
    Returns None if the input is None.
    """
    if text is None:
        return None
    text = str(text).lower()  # Ensure it's a string before lower()
    text = text.strip()
    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespace with single space
    return text
