# isdayoff — Production Calendar API Client

## About

**isdayoff** — Python library for checking whether a date is a working day or day off according to official production calendars. A thin client for the [isdayoff.ru](https://isdayoff.ru) API.

**Author:** Aleksandr Bevz (as-bivz@yandex.ru)
**License:** MIT
**Repository:** https://github.com/asbevz/isdayoff
**PyPI:** https://pypi.org/project/isdayoff-api/
**Original:** https://github.com/kobylinsky-m/isdayoff

---

## Project Structure

```
isdayoff/
├── isdayoff/
│   ├── __init__.py       # Exports: ProdCalendar, SyncProdCalendar, DateType
│   ├── isdayoff.py       # Both clients (async + sync)
│   └── typingapi.py      # Types, exceptions, pydantic models
├── tests/
│   ├── __init__.py
│   └── test_isdayoff.py  # 48 tests (40 unit + 8 integration)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml        # CI: test on push/PR (Python 3.11–3.14)
│   │   └── release.yml   # CD: publish on tag v*.*.*
│   └── dependabot.yml    # Weekly dep updates
├── pyproject.toml        # hatchling + uv
├── CHANGELOG.md
├── README.md
├── LICENSE
├── AGENTS.md
└── .gitignore
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| HTTP Client | `httpx` (async + sync) |
| Validation | `pydantic` v2 |
| Build | `hatchling` / `uv` |
| Tests | `pytest` + `pytest-asyncio` |

### Dependencies

- `httpx >= 0.28`
- `pydantic >= 2`

### Dev Dependencies

- `pytest >= 8`
- `pytest-asyncio >= 0.24`

---

## Architecture

### Two Clients

Both classes in `isdayoff.py` share the same API:

| Class | HTTP Client | Methods |
|---|---|---|
| `ProdCalendar` | `httpx.AsyncClient` | `async` |
| `SyncProdCalendar` | `httpx.Client` | sync |

Shared module-level helpers:
- `_validate_locale()` — country code validation
- `_format_result()` — parses API response into `dict[str, DateType]`
- `_build_params()` — builds query params via pydantic model

### `typingapi.py`

**`DateType` (IntEnum):** `WORKING=0`, `NOT_WORKING=1`, `SHORTENED=2`, `WORKING_DAY=4`

**`ProdCalendarParams` (pydantic.BaseModel):** Validates `locale`, `pre`, `sd`, `covid`. Method `to_api_params()` → dict.

**Exceptions:** `ServiceNotRespond` (status ≠ 200), `DataError` (400 Bad Request)

### Supported Locales

`ru`, `kz`, `by`, `us`, `uz`, `tr`, `lv`

---

## Development Commands

```bash
uv sync              # Install all deps + dev
uv run pytest -v     # Run 40 unit tests (no API calls)
uv run pytest -v -m integration  # Run 8 integration tests (real API)
uv build             # Build sdist + wheel
uv publish           # Publish to PyPI
```

---

## Conventions for AI Agents

### Code Style
- **Python 3.11+**: `from __future__ import annotations`, `TypedDict` from `typing`
- **Type hints**: Required for all public methods and functions
- **Async/Sync**: `ProdCalendar` (async) and `SyncProdCalendar` (sync) — identical public API

### Testing
- Unit tests mock `_get` via `unittest.mock.patch.object(calendar, "_get", ...)`
- Integration tests hit real API, marked with `@pytest.mark.integration`
- New features require both unit and integration tests for both clients

### Release Process
1. Bump version in: `__init__.py`, `isdayoff.py` (2×), `pyproject.toml`, `CHANGELOG.md`
2. Commit: `git commit -m "Bump to vX.Y.Z"`
3. Push commit: `git push`
4. Tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z`
5. CI runs tests; CD publishes to PyPI + creates GitHub Release

### Current Version
`1.0.2`
