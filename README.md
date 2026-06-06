<div align="center">

# 🗓️ isdayoff-api

**Production Calendar API Client**

[![PyPI - Version](https://img.shields.io/pypi/v/isdayoff-api?color=blue&style=flat-square)](https://pypi.org/project/isdayoff-api/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/isdayoff-api?color=blue&style=flat-square)](https://pypi.org/project/isdayoff-api/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/isdayoff-api?color=blue&style=flat-square)](https://pypi.org/project/isdayoff-api/)
[![GitHub License](https://img.shields.io/github/license/asbevz/isdayoff?style=flat-square)](LICENSE)
[![CI](https://github.com/asbevz/isdayoff/actions/workflows/ci.yml/badge.svg?style=flat-square)](https://github.com/asbevz/isdayoff/actions/workflows/ci.yml)

🐍 **Async** + **Sync** Python client for [isdayoff.ru](https://isdayoff.ru) – production calendar data for 7 countries.

Check if a date is a working day, a day off, or a shortened day according to official government decrees.

> This is a fork of the original [kobylinsky-m/isdayoff](https://github.com/kobylinsky-m/isdayoff).

</div>

---

## 📦 Installation

```bash
pip install isdayoff-api
```

Requires **Python 3.11+**.

---

## 🚀 Quick Start

### Async (recommended)

```python
import asyncio
from isdayoff import DateType, ProdCalendar


async def main():
    async with ProdCalendar(locale="us") as calendar:
        if await calendar.today() == DateType.WORKING:
            print("Today is a working day ✅")
        else:
            print("Today is a day off 🎉")


asyncio.run(main())
```

### Sync

```python
from isdayoff import DateType, SyncProdCalendar


with SyncProdCalendar(locale="us") as calendar:
    if calendar.today() == DateType.WORKING:
        print("Today is a working day ✅")
    else:
        print("Today is a day off 🎉")
```

---

## 🌍 Supported Locales

| Code | Country |
|------|---------|
| `ru` | Russia |
| `kz` | Kazakhstan |
| `by` | Belarus |
| `us` | United States |
| `uz` | Uzbekistan |
| `tr` | Turkey |
| `lv` | Latvia |

---

## 📖 API Reference

All methods are available on both `ProdCalendar` (async) and `SyncProdCalendar` (sync).

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `locale` | `str` | `"ru"` | Country code |
| `pre` | `bool` | `False` | Mark shortened pre‑holiday days |
| `covid` | `bool` | `False` | Mark working days due to COVID‑19 |
| `sd` | `bool` | `False` | Consider 6‑day work week |

### Methods

```python
# ── Async ──
await calendar.today(locale="ru", pre=True, covid=True, sd=True)
await calendar.tomorrow()
await calendar.date(date(2024, 8, 25))
await calendar.month(date(2024, 8, 1))
await calendar.year(date(2024, 1, 1))
await calendar.range_date(date(2024, 1, 1), date(2024, 5, 1))
calendar.is_leap(date(2024, 1, 1))

# ── Sync ──
calendar.today(locale="ru", pre=True, covid=True, sd=True)
calendar.tomorrow()
calendar.date(date(2024, 8, 25))
calendar.month(date(2024, 8, 1))
calendar.year(date(2024, 1, 1))
calendar.range_date(date(2024, 1, 1), date(2024, 5, 1))
calendar.is_leap(date(2024, 1, 1))
```

### Return Types

| Method | Returns |
|---|---|
| `today()` / `tomorrow()` / `date()` | `DateType` (enum) |
| `month()` / `year()` / `range_date()` | `dict[str, DateType]` — ISO date → type |
| `is_leap()` | `bool` |

### DateType Enum

| Value | Meaning |
|---|---|
| `DateType.WORKING` (0) | Working day |
| `DateType.NOT_WORKING` (1) | Day off / holiday |
| `DateType.SHORTENED` (2) | Shortened pre‑holiday day |
| `DateType.WORKING_DAY` (4) | Working day (special period, e.g. COVID) |

---

## 📋 Full Example

```python
import asyncio
from datetime import date
from isdayoff import DateType, ProdCalendar


async def main():
    async with ProdCalendar(locale="us") as calendar:
        month_data = await calendar.month(date(2024, 8, 1), locale="ru")
        days_off = sum(1 for v in month_data.values() if v == DateType.NOT_WORKING)
        print(f"Days off in August 2024 (RU): {days_off}")


asyncio.run(main())
```

---

## 🛠 Development

```bash
# Install dependencies
uv sync

# Run unit tests (mocked, no API calls)
uv run pytest

# Run integration tests (real API calls)
uv run pytest -m integration

# Build package
uv build
```

### Test Suite

| Type | Count | Command |
|------|-------|---------|
| 🔬 Unit | 40 | `uv run pytest` |
| 🌐 Integration | 8 | `uv run pytest -m integration` |

---

## 🔗 Links

- **Original project:** [kobylinsky-m/isdayoff](https://github.com/kobylinsky-m/isdayoff)
- **API documentation:** [isdayoff.ru/docs](https://www.isdayoff.ru/docs/)
- **Database of countries:** [isdayoff.ru/db](https://www.isdayoff.ru/db/)
- **PyPI:** [isdayoff-api](https://pypi.org/project/isdayoff-api/)

---

## 📄 License

[MIT](LICENSE)

© 2021 Maxim Kobylinsky (original author) · © 2026 [Aleksandr Bevz](https://github.com/asbevz)

---

<div align="center">
<small>Data provided by <a href="https://isdayoff.ru">isdayoff.ru</a></small>
</div>
