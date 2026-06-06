<div align="center">

# 🗓️ isdayoff-api

**Production Calendar API Client** · *Проверка дат на рабочие/нерабочие дни*

[![PyPI - Version](https://img.shields.io/pypi/v/isdayoff-api?color=blue&style=flat-square)](https://pypi.org/project/isdayoff-api/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/isdayoff-api?color=blue&style=flat-square)](https://pypi.org/project/isdayoff-api/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/isdayoff-api?color=blue&style=flat-square)](https://pypi.org/project/isdayoff-api/)
[![GitHub License](https://img.shields.io/github/license/asbevz/isdayoff?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-48%20passed-green?style=flat-square)](tests/)
[![Code style](https://img.shields.io/badge/code%20style-ruff-black?style=flat-square)](https://github.com/astral-sh/ruff)

🐍 **Async** + **Sync** клиент для [isdayoff.ru](https://isdayoff.ru) – данные по производственным календарям 7 стран.

</div>

---

## 📦 Установка

```bash
pip install isdayoff-api
```

Требуется **Python 3.11+**.

---

## 🚀 Быстрый старт

### Async (рекомендуется)

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

## 🌍 Поддерживаемые локали

| Флаг | Код | Страна |
|------|------|--------|
| 🇷🇺 | `ru` | Россия |
| 🇰🇿 | `kz` | Казахстан |
| 🇧🇾 | `by` | Беларусь |
| 🇺🇸 | `us` | США |
| 🇺🇿 | `uz` | Узбекистан |
| 🇹🇷 | `tr` | Турция |
| 🇱🇻 | `lv` | Латвия |

---

## 📖 API

Все методы доступны на обоих клиентах: `ProdCalendar` (async) и `SyncProdCalendar` (sync).

### Параметры

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `locale` | `str` | `"ru"` | Код страны |
| `pre` | `bool` | `False` | Отмечать сокращённые предпраздничные дни |
| `covid` | `bool` | `False` | Отмечать рабочие дни из‑за COVID‑19 |
| `sd` | `bool` | `False` | Шестидневная рабочая неделя |

### Методы

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

### Типы возвращаемых значений

| Метод | Возвращает |
|-------|-----------|
| `today()` / `tomorrow()` / `date()` | `DateType` (enum) |
| `month()` / `year()` / `range_date()` | `dict[str, DateType]` — ISO‑дата → тип |
| `is_leap()` | `bool` |

### DateType

| Значение | Значение | Цвет |
|----------|----------|------|
| `DateType.WORKING` (0) | Рабочий день | ✅ |
| `DateType.NOT_WORKING` (1) | Выходной / праздник | 🚫 |
| `DateType.SHORTENED` (2) | Сокращённый предпраздничный | ⏳ |
| `DateType.WORKING_DAY` (4) | Рабочий (особый период, COVID) | 🏥 |

---

## 📋 Пример

```python
import asyncio
from datetime import date
from isdayoff import DateType, ProdCalendar


async def main():
    async with ProdCalendar(locale="us") as calendar:
        month_data = await calendar.month(date(2024, 8, 1), locale="ru")
        days_off = sum(1 for v in month_data.values() if v == DateType.NOT_WORKING)
        print(f"🇷🇺 Выходных в августе 2024: {days_off}")


asyncio.run(main())
```

---

## 🛠 Разработка

```bash
# Установка зависимостей
uv sync

# Модульные тесты (без обращений к API)
uv run pytest

# Интеграционные тесты (реальное API)
uv run pytest -m integration

# Сборка пакета
uv build
```

### Структура тестов

| Тип | Кол‑во | Команда |
|-----|--------|---------|
| 🔬 Модульные | 40 | `uv run pytest` |
| 🌐 Интеграционные | 8 | `uv run pytest -m integration` |

---

## 📄 Лицензия

[MIT](LICENSE) © 2021 Максим Кобылинский · © 2026 [Aleksandr Bevz](https://github.com/asbevz)

---

<div align="center">
<small>Данные предоставлены <a href="https://isdayoff.ru">isdayoff.ru</a></small>
</div>
