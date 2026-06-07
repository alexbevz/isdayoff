# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] — 2026-06-07

### Added
- Donate block with crypto addresses in README

## [1.0.2] — 2026-06-06

### Added
- CI/CD via GitHub Actions (test matrix 3.11–3.14, auto-publish on tag)
- Dependabot for weekly dependency updates
- Python 3.14 classifier and CI support

## [1.0.1] — 2026-06-06

### Changed
- Documentation fully translated to English
- README badges and modern formatting

## [1.0.0] — 2026-06-06

Fork of the original `isdayoff` by Maxim Kobylinsky. Complete modernization of the project.

### Added
- Sync client `SyncProdCalendar` using `httpx.Client`
- Async context manager (`async with ProdCalendar()`)
- Sync context manager (`with SyncProdCalendar()`)
- Parameter validation via `pydantic.BaseModel` (`ProdCalendarParams`)
- 40 unit tests (pytest + unittest.mock)
- 8 integration tests (real API, `@pytest.mark.integration`)
- Python 3.11–3.13 support
- CHANGELOG.md

### Changed
- **Switched to `httpx`** — replaced `aiohttp` with `httpx` (async + sync in one package)
- **Switched to `pyproject.toml`** — removed `setup.py` and `requirements.txt`, build via hatchling
- **Dependency management** — `uv` instead of `pip`
- **Date format** — defaults to ISO 8601 (`%Y-%m-%d`) instead of `%Y.%m.%d`
- **Dates via `datetime.date.today()`** instead of `datetime.datetime.now()`
- **Lazy HTTP session** — client created on first request
- **System SSL** — removed insecure `ssl=False`

### Removed
- Dependencies: `aiohttp`, `typing-extensions`, `idna-ssl`
- Deprecated asyncio patterns (`get_event_loop().run_forever()`)

### Fixed
- `__init__` and `close()` now return `None`, not `NoReturn`
- Version follows PEP 440 (`"1.0.0"` instead of `1.0`)

### Locales
- Removed: `ua` (not supported by API)
- Added: `uz` (Uzbekistan), `tr` (Turkey), `lv` (Latvia)

---

## Original release

The original `isdayoff` package was created by [Maxim Kobylinsky](https://github.com/kobylinsky-m/isdayoff).
