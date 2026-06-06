# isdayoff

Production Calendar API

Description:
* Checking the date for belonging to a non-working day, according to official decrees and orders.

Official API website — https://isdayoff.ru

## Install

```bash
pip install isdayoff
```

Requires Python 3.11+.

## Supported locales

| Code | Country |
|------|---------|
| `ru` | Russia |
| `kz` | Kazakhstan |
| `by` | Belarus |
| `us` | USA |
| `uz` | Uzbekistan |
| `tr` | Turkey |
| `lv` | Latvia |

## Quick start

### Async (recommended)

```python
import asyncio
from datetime import date

from isdayoff import DateType, ProdCalendar


async def main():
    async with ProdCalendar(locale="us") as calendar:
        if await calendar.today() == DateType.WORKING:
            print("Today is a working day")
        else:
            print("Today is a day off")


asyncio.run(main())
```

### Sync

```python
from datetime import date

from isdayoff import DateType, SyncProdCalendar


with SyncProdCalendar(locale="us") as calendar:
    if calendar.today() == DateType.WORKING:
        print("Today is a working day")
    else:
        print("Today is a day off")
```

## API

All methods are available on both `ProdCalendar` (async) and `SyncProdCalendar` (sync).

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `locale` | `str` | `"ru"` | Country code (see table above) |
| `pre` | `bool` | `False` | Mark shortened working days |
| `covid` | `bool` | `False` | Mark working days due to COVID-19 |
| `sd` | `bool` | `False` | Consider 6-day work week |

### Methods

```python
# Async
await calendar.today(locale="ru", pre=True, covid=True, sd=True)
await calendar.tomorrow()
await calendar.date(date(2024, 8, 25))
await calendar.month(date(2024, 8, 1))
await calendar.year(date(2024, 1, 1))
await calendar.range_date(date(2024, 1, 1), date(2024, 5, 1))
calendar.is_leap(date(2024, 1, 1))

# Sync
calendar.today(locale="ru", pre=True, covid=True, sd=True)
calendar.tomorrow()
calendar.date(date(2024, 8, 25))
calendar.month(date(2024, 8, 1))
calendar.year(date(2024, 1, 1))
calendar.range_date(date(2024, 1, 1), date(2024, 5, 1))
calendar.is_leap(date(2024, 1, 1))
```

### Return types

| Method | Returns |
|---|---|
| `today()` / `tomorrow()` / `date()` | `DateType` enum |
| `month()` / `year()` / `range_date()` | `dict[str, DateType]` — ISO date → type |
| `is_leap()` | `bool` |

### DateType values

| Value | Meaning |
|---|---|
| `DateType.WORKING` (0) | Working day |
| `DateType.NOT_WORKING` (1) | Day off / holiday |
| `DateType.SHORTENED` (2) | Shortened pre-holiday day |
| `DateType.WORKING_DAY` (4) | Working day (special period) |

## Full example

```python
import asyncio
from datetime import date

from isdayoff import DateType, ProdCalendar


async def main():
    async with ProdCalendar(locale="us") as calendar:
        res = await calendar.month(date(2024, 8, 1), locale="ru")
        days_off = sum(
            1 for v in res.values() if v == DateType.NOT_WORKING
        )
        print(f"Days off in August 2024: {days_off}")


asyncio.run(main())
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Build
uv build
```
