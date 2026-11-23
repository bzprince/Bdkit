"""Taka helpers: lakh/crore grouping and amount-in-words (Bangla & English)."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from .digits import to_bangla_digits

_BN_WORDS = (
    "শূন্য এক দুই তিন চার পাঁচ ছয় সাত আট নয় দশ "
    "এগারো বারো তেরো চৌদ্দ পনেরো ষোল সতেরো আঠারো উনিশ বিশ "
    "একুশ বাইশ তেইশ চব্বিশ পঁচিশ ছাব্বিশ সাতাশ আটাশ ঊনত্রিশ ত্রিশ "
    "একত্রিশ বত্রিশ তেত্রিশ চৌত্রিশ পঁইত্রিশ ছত্রিশ সাঁইত্রিশ আটত্রিশ ঊনচল্লিশ চল্লিশ "
    "একচল্লিশ বিয়াল্লিশ তেতাল্লিশ চুয়াল্লিশ পঁয়তাল্লিশ ছেচল্লিশ সাতচল্লিশ আটচল্লিশ ঊনপঞ্চাশ পঞ্চাশ "
    "একান্ন বাহান্ন তিপ্পান্ন চুয়ান্ন পঞ্চান্ন ছাপ্পান্ন সাতান্ন আটান্ন ঊনষাট ষাট "
    "একষট্টি বাষট্টি তেষট্টি চৌষট্টি পঁয়ষট্টি ছেষট্টি সাতষট্টি আটষট্টি ঊনসত্তর সত্তর "
    "একাত্তর বাহাত্তর তিয়াত্তর চুয়াত্তর পঁচাত্তর ছিয়াত্তর সাতাত্তর আটাত্তর ঊনআশি আশি "
    "একাশি বিরাশি তিরাশি চুরাশি পঁচাশি ছিয়াশি সাতাশি আটাশি ঊননব্বই নব্বই "
    "একানব্বই বিরানব্বই তিরানব্বই চুরানব্বই পঁচানব্বই ছিয়ানব্বই সাতানব্বই আটানব্বই নিরানব্বই"
).split()
assert len(_BN_WORDS) == 100

_EN_ONES = (
    "Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen "
    "Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen"
).split()
_EN_TENS = "_ _ Twenty Thirty Forty Fifty Sixty Seventy Eighty Ninety".split()


def _en_below_100(n: int) -> str:
    if n < 20:
        return _EN_ONES[n]
    tens, ones = divmod(n, 10)
    return _EN_TENS[tens] + (f" {_EN_ONES[ones]}" if ones else "")


def _words(n: int, below_100, units) -> str:
    """South-Asian grouping: crore, lakh, thousand, hundred."""
    crore_u, lakh_u, thou_u, hund_u = units
    parts = []
    crore, n = divmod(n, 10**7)
    if crore:
        parts.append(f"{_words(crore, below_100, units)} {crore_u}")
    lakh, n = divmod(n, 10**5)
    if lakh:
        parts.append(f"{below_100(lakh)} {lakh_u}")
    thousand, n = divmod(n, 1000)
    if thousand:
        parts.append(f"{below_100(thousand)} {thou_u}")
    hundred, n = divmod(n, 100)
    if hundred:
        parts.append(f"{below_100(hundred)} {hund_u}")
    if n:
        parts.append(below_100(n))
    return " ".join(parts)


def _to_decimal(amount) -> Decimal:
    try:
        d = Decimal(str(amount))
    except InvalidOperation:
        raise ValueError(f"not a valid amount: {amount!r}") from None
    if not d.is_finite():
        raise ValueError(f"not a valid amount: {amount!r}")
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_taka(amount, bangla: bool = False, symbol: str = "৳") -> str:
    """Format with lakh/crore grouping: 1234567.5 -> '৳12,34,567.50'."""
    d = _to_decimal(amount)
    sign = "-" if d < 0 else ""
    whole, frac = f"{abs(d):.2f}".split(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        whole = ",".join(groups + [tail])
    out = f"{sign}{symbol}{whole}.{frac}"
    return to_bangla_digits(out) if bangla else out


def taka_in_words(amount, lang: str = "bn", only: bool = False) -> str:
    """Amount in words, handy for cheques/invoices.

    >>> taka_in_words(150000)
    'এক লক্ষ পঞ্চাশ হাজার টাকা'
    >>> taka_in_words(1250.5, lang="en")
    'One Thousand Two Hundred Fifty Taka and Fifty Paisa'
    """
    if lang not in ("bn", "en"):
        raise ValueError("lang must be 'bn' or 'en'")
    d = _to_decimal(amount)
    neg = d < 0
    d = abs(d)
    taka, paisa = int(d), int((d - int(d)) * 100)

    if lang == "bn":
        below = _BN_WORDS.__getitem__
        units = ("কোটি", "লক্ষ", "হাজার", "শত")
        zero, t_u, p_u, minus, only_w, joiner = "শূন্য", "টাকা", "পয়সা", "মাইনাস", "মাত্র", " "
    else:
        below = _en_below_100
        units = ("Crore", "Lakh", "Thousand", "Hundred")
        zero, t_u, p_u, minus, only_w, joiner = "Zero", "Taka", "Paisa", "Minus", "Only", " and "

    parts = []
    if taka or not paisa:
        parts.append(f"{_words(taka, below, units) or zero} {t_u}")
    if paisa:
        parts.append(f"{_words(paisa, below, units)} {p_u}")
    text = joiner.join(parts)
    if neg:
        text = f"{minus} {text}"
    return f"{text} {only_w}" if only else text
