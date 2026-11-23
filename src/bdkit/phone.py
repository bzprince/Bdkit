"""Bangladeshi mobile number validation, normalisation and operator lookup."""

import re
from typing import Optional

from .digits import to_english_digits

_OPERATORS = {
    "013": "Grameenphone",
    "014": "Banglalink",
    "015": "Teletalk",
    "016": "Airtel (Robi)",
    "017": "Grameenphone",
    "018": "Robi",
    "019": "Banglalink",
}


def normalize_phone(raw: str) -> Optional[str]:
    """Return '+8801XXXXXXXXX' or None if not a valid BD mobile number.

    Accepts 01712345678, +8801712345678, 8801712-345678, 008801712345678,
    and Bangla digits.
    """
    s = re.sub(r"[\s\-().]", "", to_english_digits(raw))
    if s.startswith("+"):
        s = s[1:]
    if s.startswith("00880"):
        s = s[2:]
    if s.startswith("880"):
        s = "0" + s[3:]
    if re.fullmatch(r"01[3-9]\d{8}", s):
        return "+88" + s
    return None


def is_valid_phone(raw: str) -> bool:
    return normalize_phone(raw) is not None


def operator(raw: str) -> Optional[str]:
    """Operator name from the prefix, or None for invalid numbers.

    Note: number portability means this is a hint, not a guarantee.
    """
    n = normalize_phone(raw)
    return _OPERATORS[n[3:6]] if n else None
