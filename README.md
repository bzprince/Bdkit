# bdkit 🇧🇩

Tiny, zero-dependency Python utilities for Bangladesh-focused apps.

- **Taka in words** (বাংলা & English) — for invoices and cheques
- **Lakh/crore formatting** — `৳12,34,567.50`
- **Bangla ⇄ English digits**
- **BD mobile number** validation, normalisation, operator lookup
- **Divisions** with Bangla names

## Install

```bash
pip install git+https://github.com/YOUR_USERNAME/bdkit.git
```

## Usage

```python
from bdkit import *

taka_in_words(150000)               # 'এক লক্ষ পঞ্চাশ হাজার টাকা'
taka_in_words(1250.5, lang="en")    # 'One Thousand Two Hundred Fifty Taka and Fifty Paisa'
taka_in_words(10, lang="en", only=True)  # 'Ten Taka Only'

format_taka(1234567.5)              # '৳12,34,567.50'
format_taka(45000, bangla=True)     # '৳৪৫,০০০.০০'

to_bangla_digits(2026)              # '২০২৬'
to_english_digits("০১৭১২")           # '01712'

normalize_phone("01712-345678")     # '+8801712345678'
is_valid_phone("+8801812345678")    # True
operator("01512345678")             # 'Teletalk'

DIVISIONS["Sylhet"]                 # 'সিলেট'
```

## Notes

- Amounts use `Decimal` internally, rounded half-up to 2 places (paisa).
- `operator()` reads the prefix only; number portability means it is a hint.

## Development

```bash
pip install -e . pytest
pytest
```

## Roadmap

- [ ] Bangla calendar (বঙ্গাব্দ) date conversion
- [ ] 64 districts + upazilas dataset
- [ ] NID format validation
- [ ] Bangla ordinal numbers (১ম, ২য়, ৩য়…)

PRs welcome. MIT licensed.
