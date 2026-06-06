from __future__ import annotations

import datetime
from typing import Any

import httpx

from .typingapi import (
    DataError,
    DateType,
    ProdCalendarParams,
    ServiceNotRespond,
)

_LOCALES = ("ru", "kz", "by", "us", "uz", "tr", "lv")
_DELIMITER = "%7C"
_FORMAT_DATE = "%Y%m%d"


# ── shared helpers ───────────────────────────────────────────────────────────


def _validate_locale(locale: str) -> str:
    if locale not in _LOCALES:
        msg = f"locale must be one of {_LOCALES}, got {locale!r}"
        raise ValueError(msg)
    return locale


def _format_result(
    date_format: str, date: datetime.date, result: list[str]
) -> dict[str, DateType]:
    return {
        (date + datetime.timedelta(days=day)).strftime(date_format): DateType(int(value))
        for day, value in enumerate(result)
    }


def _build_params(locale: str, **kwargs: Any) -> dict[str, Any]:
    params = ProdCalendarParams(**kwargs)
    api_params = params.to_api_params()
    api_params.setdefault("cc", locale)
    return api_params


# ── async client ─────────────────────────────────────────────────────────────


class ProdCalendar:
    """Async production calendar client using httpx.AsyncClient."""

    __version__ = "1.0.1"

    def __init__(
        self,
        locale: str = "ru",
        base_url: str = "https://isdayoff.ru",
        date_format: str = "%Y-%m-%d",
    ) -> None:
        self.date_format = date_format
        self.locale = _validate_locale(locale)
        self.base_url = base_url.rstrip("/")
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers={
                    "User-Agent": (
                        f"isdayoff/{self.__version__} "
                        "Contact: wg7831@gmail.com"
                    )
                },
            )
        return self._client

    async def _get(
        self, url: str, params: dict[str, Any] | None = None
    ) -> str:
        client = await self._get_client()
        response = await client.get(self.base_url + url, params=params)
        if response.status_code == 400:
            raise DataError("Date error")
        if response.status_code != 200:
            raise ServiceNotRespond("No data found")
        return response.text

    async def _get_date_work(
        self,
        data: datetime.date,
        is_day: bool = True,
        is_month: bool = True,
        **kwargs: Any,
    ) -> str:
        params = _build_params(self.locale, **kwargs)
        params["year"] = data.year
        if is_month:
            params["month"] = data.month
        if is_day:
            params["day"] = data.day
        if not (is_month and is_day):
            params["delimeter"] = _DELIMITER
        return await self._get("/api/getdata", params=params)

    async def _get_range_date_work(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        **kwargs: Any,
    ) -> str:
        params = _build_params(self.locale, **kwargs)
        params["date1"] = start_date.strftime(_FORMAT_DATE)
        params["date2"] = end_date.strftime(_FORMAT_DATE)
        params["delimeter"] = _DELIMITER
        return await self._get("/api/getdata", params=params)

    async def _get_date_as_type(
        self, date: datetime.date, **kwargs: Any
    ) -> DateType:
        raw = await self._get_date_work(date, **kwargs)
        return DateType(int(raw))

    async def range_date(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        **kwargs: Any,
    ) -> dict[str, DateType]:
        result = (await self._get_range_date_work(start_date, end_date, **kwargs)).split(
            _DELIMITER,
        )
        return _format_result(self.date_format, start_date, result)

    async def month(
        self, date: datetime.date, **kwargs: Any
    ) -> dict[str, DateType]:
        result = (
            await self._get_date_work(date, is_day=False, **kwargs)
        ).split(_DELIMITER)
        return _format_result(
            self.date_format, datetime.date(date.year, date.month, 1), result,
        )

    async def year(
        self, date: datetime.date, **kwargs: Any
    ) -> dict[str, DateType]:
        result = (
            await self._get_date_work(date, is_day=False, is_month=False, **kwargs)
        ).split(_DELIMITER)
        return _format_result(self.date_format, datetime.date(date.year, 1, 1), result)

    async def date(self, date: datetime.date, **kwargs: Any) -> DateType:
        return await self._get_date_as_type(date, **kwargs)

    async def tomorrow(self, **kwargs: Any) -> DateType:
        return await self._get_date_as_type(
            datetime.date.today() + datetime.timedelta(days=1),
            **kwargs,
        )

    async def today(self, **kwargs: Any) -> DateType:
        return await self._get_date_as_type(datetime.date.today(), **kwargs)

    @staticmethod
    def is_leap(date: datetime.date) -> bool:
        return date.year % 4 == 0 and date.year % 100 != 0 or date.year % 400 == 0

    async def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self) -> ProdCalendar:
        await self._get_client()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        await self.close()


# ── sync client ──────────────────────────────────────────────────────────────


class SyncProdCalendar:
    """Sync production calendar client using httpx.Client."""

    __version__ = "1.0.1"

    def __init__(
        self,
        locale: str = "ru",
        base_url: str = "https://isdayoff.ru",
        date_format: str = "%Y-%m-%d",
    ) -> None:
        self.date_format = date_format
        self.locale = _validate_locale(locale)
        self.base_url = base_url.rstrip("/")
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                headers={
                    "User-Agent": (
                        f"isdayoff/{self.__version__} "
                        "Contact: wg7831@gmail.com"
                    )
                },
            )
        return self._client

    def _get(
        self, url: str, params: dict[str, Any] | None = None
    ) -> str:
        client = self._get_client()
        response = client.get(self.base_url + url, params=params)
        if response.status_code == 400:
            raise DataError("Date error")
        if response.status_code != 200:
            raise ServiceNotRespond("No data found")
        return response.text

    def _get_date_work(
        self,
        data: datetime.date,
        is_day: bool = True,
        is_month: bool = True,
        **kwargs: Any,
    ) -> str:
        params = _build_params(self.locale, **kwargs)
        params["year"] = data.year
        if is_month:
            params["month"] = data.month
        if is_day:
            params["day"] = data.day
        if not (is_month and is_day):
            params["delimeter"] = _DELIMITER
        return self._get("/api/getdata", params=params)

    def _get_range_date_work(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        **kwargs: Any,
    ) -> str:
        params = _build_params(self.locale, **kwargs)
        params["date1"] = start_date.strftime(_FORMAT_DATE)
        params["date2"] = end_date.strftime(_FORMAT_DATE)
        params["delimeter"] = _DELIMITER
        return self._get("/api/getdata", params=params)

    def _get_date_as_type(
        self, date: datetime.date, **kwargs: Any
    ) -> DateType:
        raw = self._get_date_work(date, **kwargs)
        return DateType(int(raw))

    def range_date(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        **kwargs: Any,
    ) -> dict[str, DateType]:
        result = self._get_range_date_work(start_date, end_date, **kwargs).split(
            _DELIMITER,
        )
        return _format_result(self.date_format, start_date, result)

    def month(
        self, date: datetime.date, **kwargs: Any
    ) -> dict[str, DateType]:
        result = self._get_date_work(date, is_day=False, **kwargs).split(_DELIMITER)
        return _format_result(
            self.date_format, datetime.date(date.year, date.month, 1), result,
        )

    def year(
        self, date: datetime.date, **kwargs: Any
    ) -> dict[str, DateType]:
        result = self._get_date_work(
            date, is_day=False, is_month=False, **kwargs
        ).split(_DELIMITER)
        return _format_result(self.date_format, datetime.date(date.year, 1, 1), result)

    def date(self, date: datetime.date, **kwargs: Any) -> DateType:
        return self._get_date_as_type(date, **kwargs)

    def tomorrow(self, **kwargs: Any) -> DateType:
        return self._get_date_as_type(
            datetime.date.today() + datetime.timedelta(days=1),
            **kwargs,
        )

    def today(self, **kwargs: Any) -> DateType:
        return self._get_date_as_type(datetime.date.today(), **kwargs)

    @staticmethod
    def is_leap(date: datetime.date) -> bool:
        return date.year % 4 == 0 and date.year % 100 != 0 or date.year % 400 == 0

    def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            self._client.close()

    def __enter__(self) -> SyncProdCalendar:
        self._get_client()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self.close()
