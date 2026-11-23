"""bdkit - tiny zero-dependency utilities for Bangladesh-focused apps."""

from .digits import to_bangla_digits, to_english_digits
from .geo import DIVISIONS
from .money import format_taka, taka_in_words
from .phone import is_valid_phone, normalize_phone, operator

__version__ = "0.1.0"
__all__ = [
    "to_bangla_digits", "to_english_digits", "format_taka", "taka_in_words",
    "normalize_phone", "is_valid_phone", "operator", "DIVISIONS",
]
