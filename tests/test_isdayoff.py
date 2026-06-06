from __future__ import annotations

import datetime
from unittest.mock import ANY, AsyncMock, patch

import httpx
import pytest

from isdayoff import DateType, ProdCalendar, SyncProdCalendar
from isdayoff.typingapi import DataError, ServiceNotRespond


# ── fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def calendar() -> ProdCalendar:
    return ProdCalendar(locale="ru")


@pytest.fixture
def sync_calendar() -> SyncProdCalendar:
    return SyncProdCalendar(locale="ru")


# ── helper: mock httpx response ──────────────────────────────────────────────


def _mock_httpx_response(text: str = "0", status_code: int = 200) -> httpx.Response:
    """Build a minimal httpx.Response with the given text/status."""
    return httpx.Response(status_code=status_code, text=text)


# ═══════════════════════════════════════════════════════════════════════════════
# Async ProdCalendar tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestProdCalendar:
    """Async client tests."""

    # ── single-date methods ──────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_today_working(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="0"):
            result = await calendar.today()
        assert result == DateType.WORKING

    @pytest.mark.asyncio
    async def test_today_not_working(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="1"):
            result = await calendar.today()
        assert result == DateType.NOT_WORKING

    @pytest.mark.asyncio
    async def test_today_shortened(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="2"):
            result = await calendar.today()
        assert result == DateType.SHORTENED

    @pytest.mark.asyncio
    async def test_today_working_covid(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="4"):
            result = await calendar.today()
        assert result == DateType.WORKING_DAY

    @pytest.mark.asyncio
    async def test_date_specific(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="1"):
            result = await calendar.date(datetime.date(2024, 1, 1))
        assert result == DateType.NOT_WORKING

    @pytest.mark.asyncio
    async def test_tomorrow(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="0"):
            result = await calendar.tomorrow()
        assert result == DateType.WORKING

    # ── range methods ───────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_month(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="0%7C1%7C0%7C1%7C0%7C1%7C0"):
            result = await calendar.month(datetime.date(2024, 1, 1))
        assert isinstance(result, dict)
        first_key = min(result.keys())
        assert first_key == "2024-01-01"
        assert result["2024-01-01"] == DateType.WORKING
        assert result["2024-01-02"] == DateType.NOT_WORKING

    @pytest.mark.asyncio
    async def test_year(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="0%7C0%7C0"):
            result = await calendar.year(datetime.date(2024, 1, 1))
        first_key = min(result.keys())
        assert first_key == "2024-01-01"
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_range_date(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="0%7C1%7C0"):
            result = await calendar.range_date(
                datetime.date(2024, 1, 1), datetime.date(2024, 1, 3),
            )
        assert len(result) == 3
        assert result["2024-01-01"] == DateType.WORKING
        assert result["2024-01-02"] == DateType.NOT_WORKING

    # ── locale ──────────────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_locale_us_working(self) -> None:
        cal = ProdCalendar(locale="us")
        with patch.object(cal, "_get", return_value="0"):
            result = await cal.today()
        assert result == DateType.WORKING

    # ── error handling ──────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_data_error(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", side_effect=DataError("Date error")):
            with pytest.raises(DataError, match="Date error"):
                await calendar.today()

    @pytest.mark.asyncio
    async def test_service_not_respond(self, calendar: ProdCalendar) -> None:
        with patch.object(
            calendar, "_get", side_effect=ServiceNotRespond("No data found")
        ):
            with pytest.raises(ServiceNotRespond, match="No data found"):
                await calendar.today()

    # ── context manager ────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        async with ProdCalendar(locale="ru") as cal:
            assert isinstance(cal, ProdCalendar)
            assert cal._client is not None
        assert cal._client.is_closed

    # ── date format ─────────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_custom_date_format(self) -> None:
        cal = ProdCalendar(locale="ru", date_format="%d.%m.%Y")
        with patch.object(cal, "_get", return_value="0%7C1"):
            result = await cal.month(datetime.date(2024, 1, 1))
        first_key = min(result.keys())
        assert first_key == "01.01.2024"

    @pytest.mark.asyncio
    async def test_default_date_format_is_iso(self) -> None:
        cal = ProdCalendar(locale="ru")
        with patch.object(cal, "_get", return_value="0"):
            result = await cal.month(datetime.date(2024, 1, 1))
        first_key = min(result.keys())
        assert first_key == "2024-01-01"

    # ── kwargs ──────────────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_kwargs_passed(self, calendar: ProdCalendar) -> None:
        with patch.object(calendar, "_get", return_value="0") as mock_get:
            result = await calendar.today(pre=True, sd=True, covid=True)
        assert result == DateType.WORKING


# ═══════════════════════════════════════════════════════════════════════════════
# Sync SyncProdCalendar tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestSyncProdCalendar:
    """Sync client tests."""

    # ── single-date methods ──────────────────────────────────────────────

    def test_today_working(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="0"):
            result = sync_calendar.today()
        assert result == DateType.WORKING

    def test_today_not_working(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="1"):
            result = sync_calendar.today()
        assert result == DateType.NOT_WORKING

    def test_today_shortened(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="2"):
            result = sync_calendar.today()
        assert result == DateType.SHORTENED

    def test_today_working_covid(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="4"):
            result = sync_calendar.today()
        assert result == DateType.WORKING_DAY

    def test_date_specific(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="1"):
            result = sync_calendar.date(datetime.date(2024, 1, 1))
        assert result == DateType.NOT_WORKING

    def test_tomorrow(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="0"):
            result = sync_calendar.tomorrow()
        assert result == DateType.WORKING

    # ── range methods ───────────────────────────────────────────────────

    def test_month(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="0%7C1%7C0%7C1%7C0%7C1%7C0"):
            result = sync_calendar.month(datetime.date(2024, 1, 1))
        assert isinstance(result, dict)
        first_key = min(result.keys())
        assert first_key == "2024-01-01"
        assert result["2024-01-01"] == DateType.WORKING
        assert result["2024-01-02"] == DateType.NOT_WORKING

    def test_year(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="0%7C0%7C0"):
            result = sync_calendar.year(datetime.date(2024, 1, 1))
        first_key = min(result.keys())
        assert first_key == "2024-01-01"
        assert len(result) == 3

    def test_range_date(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="0%7C1%7C0"):
            result = sync_calendar.range_date(
                datetime.date(2024, 1, 1), datetime.date(2024, 1, 3),
            )
        assert len(result) == 3
        assert result["2024-01-01"] == DateType.WORKING
        assert result["2024-01-02"] == DateType.NOT_WORKING

    # ── locale ──────────────────────────────────────────────────────────

    def test_locale_us_working(self) -> None:
        cal = SyncProdCalendar(locale="us")
        with patch.object(cal, "_get", return_value="0"):
            result = cal.today()
        assert result == DateType.WORKING

    # ── error handling ──────────────────────────────────────────────────

    def test_data_error(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(
            sync_calendar, "_get", side_effect=DataError("Date error")
        ):
            with pytest.raises(DataError, match="Date error"):
                sync_calendar.today()

    def test_service_not_respond(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(
            sync_calendar, "_get", side_effect=ServiceNotRespond("No data found")
        ):
            with pytest.raises(ServiceNotRespond, match="No data found"):
                sync_calendar.today()

    # ── context manager ────────────────────────────────────────────────

    def test_sync_context_manager(self) -> None:
        with SyncProdCalendar(locale="ru") as cal:
            assert isinstance(cal, SyncProdCalendar)
            assert cal._client is not None
        assert cal._client.is_closed

    # ── date format ─────────────────────────────────────────────────────

    def test_custom_date_format(self) -> None:
        cal = SyncProdCalendar(locale="ru", date_format="%d.%m.%Y")
        with patch.object(cal, "_get", return_value="0%7C1"):
            result = cal.month(datetime.date(2024, 1, 1))
        first_key = min(result.keys())
        assert first_key == "01.01.2024"

    def test_default_date_format_is_iso(self) -> None:
        cal = SyncProdCalendar(locale="ru")
        with patch.object(cal, "_get", return_value="0"):
            result = cal.month(datetime.date(2024, 1, 1))
        first_key = min(result.keys())
        assert first_key == "2024-01-01"

    # ── kwargs ──────────────────────────────────────────────────────────

    def test_kwargs_passed(self, sync_calendar: SyncProdCalendar) -> None:
        with patch.object(sync_calendar, "_get", return_value="0") as mock_get:
            result = sync_calendar.today(pre=True, sd=True, covid=True)
        assert result == DateType.WORKING


# ═══════════════════════════════════════════════════════════════════════════════
# Shared tests (both clients)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCommon:
    """Tests that apply to both sync and async clients."""

    def test_invalid_locale(self) -> None:
        with pytest.raises(ValueError, match="locale must be one of"):
            ProdCalendar(locale="fr")
        with pytest.raises(ValueError, match="locale must be one of"):
            SyncProdCalendar(locale="fr")

    @pytest.mark.parametrize(
        ("year", "expected"),
        [
            (2020, True),
            (2021, False),
            (1900, False),
            (2000, True),
            (2024, True),
            (2025, False),
        ],
    )
    def test_is_leap(self, year: int, expected: bool) -> None:
        assert ProdCalendar.is_leap(datetime.date(year, 1, 1)) is expected
        assert SyncProdCalendar.is_leap(datetime.date(year, 1, 1)) is expected

    def test_locale_is_valid_in_constructor(self) -> None:
        cal = ProdCalendar(locale="tr")
        assert cal.locale == "tr"
        cal2 = SyncProdCalendar(locale="uz")
        assert cal2.locale == "uz"
