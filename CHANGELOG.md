# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-06-06

Форк оригинального `isdayoff` (автор: Максим Кобылинский). Полная модернизация проекта.

### Added
- Синхронный клиент `SyncProdCalendar` на `httpx.Client`
- Асинхронный контекстный менеджер (`async with ProdCalendar()`)
- Синхронный контекстный менеджер (`with SyncProdCalendar()`)
- Валидация параметров через `pydantic.BaseModel` (`ProdCalendarParams`)
- 40 модульных тестов (pytest + unittest.mock)
- 8 интеграционных тестов (реальное API, `@pytest.mark.integration`)
- Поддержка Python 3.11–3.13
- CHANGELOG.md

### Changed
- **Переход на `httpx`** — замена `aiohttp` на `httpx` (async + sync в одном пакете)
- **Переход на `pyproject.toml`** — удалены `setup.py` и `requirements.txt`, сборка через hatchling
- **Менеджер зависимостей** — `uv` вместо `pip`
- **Формат дат** — по умолчанию ISO 8601 (`%Y-%m-%d`) вместо `%Y.%m.%d`
- **Даты через `datetime.date.today()`** вместо `datetime.datetime.now()`
- **Ленивая HTTP-сессия** — клиент создаётся при первом запросе
- **Системный SSL** — удалён небезопасный `ssl=False`

### Removed
- Зависимости: `aiohttp`, `typing-extensions`, `idna-ssl`
- Устаревшие паттерны asyncio (`get_event_loop().run_forever()`)

### Fixed
- `__init__` и `close()` теперь возвращают `None`, а не `NoReturn`
- Версия приведена к PEP 440 (`"1.0.0"` вместо `1.0`)

### Locales
- Удалена: `ua` (не поддерживается API)
- Добавлены: `uz` (Узбекистан), `tr` (Турция), `lv` (Латвия)

---

## [1.0.0] — оригинальный релиз

Оригинальная версия от Максима Кобылинского (`kobylinsky-m/isdayoff`).
