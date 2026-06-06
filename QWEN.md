# isdayoff — Production Calendar API Client

## Описание проекта

**isdayoff** — Python-библиотека для проверки даты на принадлежность к рабочему/нерабочему дню согласно официальным производственным календарям. Тонкий клиент для API [isdayoff.ru](https://isdayoff.ru).

**Автор:** Максим Кобылинский (wg7831@gmail.com)
**Лицензия:** MIT
**Репозиторий:** https://github.com/kobylinsky-m/isdayoff
**PyPI:** https://pypi.org/project/isdayoff/

---

## Структура проекта

```
isdayoff/
├── isdayoff/
│   ├── __init__.py       # Экспорт: ProdCalendar, SyncProdCalendar, DateType
│   ├── isdayoff.py       # Оба клиента (async + sync)
│   └── typingapi.py      # Типы, исключения, pydantic-модели
├── tests/
│   ├── __init__.py
│   └── test_isdayoff.py  # 40 тестов (pytest)
├── pyproject.toml        # hatchling + uv
├── README.md
├── LICENSE
├── .gitignore
└── QWEN.md
```

---

## Технологии

| Компонент | Технология |
|---|---|
| Язык | Python 3.11+ |
| HTTP-клиент | `httpx` (async + sync) |
| Валидация | `pydantic` v2 |
| Сборка | `hatchling` / `uv` |
| Тесты | `pytest` + `pytest-asyncio` |

### Зависимости

```
httpx >= 0.28
pydantic >= 2
```

### Dev-зависимости

```
pytest >= 8
pytest-asyncio >= 0.24
```

---

## Архитектура

### Два клиента

В `isdayoff.py` определены два класса с идентичным API:

| Класс | HTTP-клиент | Методы |
|---|---|---|
| `ProdCalendar` | `httpx.AsyncClient` | `async` |
| `SyncProdCalendar` | `httpx.Client` | синхронные |

Оба используют общие модульные функции:
- `_validate_locale()` — валидация кода страны
- `_format_result()` — парсинг ответа API в `dict[str, DateType]`
- `_build_params()` — формирование параметров через pydantic

### `typingapi.py`

#### `DateType` (IntEnum)

| Имя | Значение |
|---|---|
| `WORKING` | 0 |
| `NOT_WORKING` | 1 |
| `SHORTENED` | 2 |
| `WORKING_DAY` | 4 |

#### `ProdCalendarParams` (pydantic.BaseModel)

Валидирует `locale`, `pre`, `sd`, `covid`. Метод `to_api_params()` → `dict`.

#### Исключения

- `ServiceNotRespond` — сервер не ответил (статус ≠ 200)
- `DataError` — ошибка в дате (400 Bad Request)

### Поддерживаемые локали

`ru`, `kz`, `by`, `us`, `uz`, `tr`, `lv`

---

## Установка и запуск

```bash
pip install isdayoff

# или для разработки:
uv sync
uv run pytest
uv build
```

### Команды uv

| Команда | Назначение |
|---|---|
| `uv sync` | Установить зависимости + dev |
| `uv run pytest -v` | Запустить 40 тестов |
| `uv build` | Собрать sdist + wheel |

---

## Разработка и Conventions

- **Python 3.11+**: `TypedDict` из `typing`, `from __future__ import annotations`
- **Два клиента**: `ProdCalendar` (async) и `SyncProdCalendar` (sync) — одинаковые методы
- **Валидация**: pydantic `BaseModel` c `field_validator` для locale
- **Версионирование**: `__version__ = "1.0.0"` (PEP 440), в `pyproject.toml` и `__init__.py`
- **Формат дат**: ISO 8601 (`%Y-%m-%d`) по умолчанию
- **HTTP-сессия**: Ленивая инициализация, автоматическое закрытие через context manager
- **User-Agent**: `isdayoff/1.0.0 Contact: wg7831@gmail.com`
- **Тесты**: мокирование `_get` через `unittest.mock.patch.object` — без реальных HTTP-запросов
- **Локали**: isdayoff.ru использует ISO 3166-1 alpha-2 коды; `ru`, `kz`, `by`, `us`, `uz`, `tr`, `lv`
