"""Bangla <-> English digit conversion."""

_BN = "০১২৩৪৫৬৭৮৯"
_EN = "0123456789"
_TO_BN = str.maketrans(_EN, _BN)
_TO_EN = str.maketrans(_BN, _EN)


def to_bangla_digits(value) -> str:
    """'2026' -> '২০২৬'. Non-digit characters are left untouched."""
    return str(value).translate(_TO_BN)


def to_english_digits(value) -> str:
    """'২০২৬' -> '2026'. Non-digit characters are left untouched."""
    return str(value).translate(_TO_EN)
