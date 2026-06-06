from __future__ import annotations

from enum import IntEnum
from typing import Any

from pydantic import BaseModel, field_validator


class ServiceNotRespond(Exception):
    """The API service did not respond or returned an unexpected status."""


class DataError(Exception):
    """Invalid date data passed to the API (400 Bad Request)."""


class DateType(IntEnum):
    WORKING = 0
    NOT_WORKING = 1
    SHORTENED = 2
    WORKING_DAY = 4


_LOCALES = ("ru", "kz", "by", "us", "uz", "tr", "lv")


class ProdCalendarParams(BaseModel):
    """Validated parameters for ProdCalendar API methods."""

    locale: str | None = None
    pre: bool = False
    sd: bool = False
    covid: bool = False

    @field_validator("locale")
    @classmethod
    def _validate_locale(cls, v: str | None) -> str | None:
        if v is not None and v not in _LOCALES:
            msg = f"locale must be one of {_LOCALES}, got {v!r}"
            raise ValueError(msg)
        return v

    def to_api_params(self) -> dict[str, Any]:
        """Convert to API query parameters, omitting falsy bools."""
        params: dict[str, Any] = {}
        if self.locale is not None:
            params["cc"] = self.locale
        if self.pre:
            params["pre"] = 1
        if self.sd:
            params["sd"] = 1
        if self.covid:
            params["covid"] = 1
        return params
