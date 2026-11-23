import pytest

from bdkit import (DIVISIONS, format_taka, is_valid_phone, normalize_phone,
                   operator, taka_in_words, to_bangla_digits, to_english_digits)


def test_digits():
    assert to_bangla_digits(2026) == "২০২৬"
    assert to_english_digits("১২৩abc") == "123abc"


def test_format_taka():
    assert format_taka(1234567.5) == "৳12,34,567.50"
    assert format_taka(999) == "৳999.00"
    assert format_taka(100000) == "৳1,00,000.00"
    assert format_taka(-45000, bangla=True) == "-৳৪৫,০০০.০০"


@pytest.mark.parametrize("amount,expected", [
    (0, "শূন্য টাকা"),
    (21, "একুশ টাকা"),
    (100, "এক শত টাকা"),
    (150000, "এক লক্ষ পঞ্চাশ হাজার টাকা"),
    (10000000, "এক কোটি টাকা"),
    (1000000000, "এক শত কোটি টাকা"),
    (12.5, "বারো টাকা পঞ্চাশ পয়সা"),
])
def test_words_bn(amount, expected):
    assert taka_in_words(amount) == expected


def test_words_en():
    assert taka_in_words(1250.5, lang="en") == "One Thousand Two Hundred Fifty Taka and Fifty Paisa"
    assert taka_in_words(0.5, lang="en") == "Fifty Paisa"
    assert taka_in_words(10, lang="en", only=True) == "Ten Taka Only"
    assert taka_in_words(-5, lang="en") == "Minus Five Taka"


def test_words_bad_input():
    with pytest.raises(ValueError):
        taka_in_words("abc")
    with pytest.raises(ValueError):
        taka_in_words(1, lang="fr")


def test_phone():
    assert normalize_phone("01712-345678") == "+8801712345678"
    assert normalize_phone("+8801812345678") == "+8801812345678"
    assert normalize_phone("০১৯১২৩৪৫৬৭৮") == "+8801912345678"
    assert normalize_phone("008801712345678") == "+8801712345678"
    assert not is_valid_phone("01212345678")
    assert not is_valid_phone("0171234567")
    assert operator("01512345678") == "Teletalk"
    assert operator("123") is None


def test_divisions():
    assert len(DIVISIONS) == 8
