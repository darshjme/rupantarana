"""DateTimeConverter — normalizes datetime representations."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Union

from .base import Converter

# Common date/time formats to try in order
_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%B %d, %Y",
    "%b %d, %Y",
    "%d %B %Y",
    "%d %b %Y",
]

# Detect numeric-only strings (Unix timestamps)
_NUMERIC_RE = re.compile(r"^\s*[+-]?\d+(\.\d+)?\s*$")


def _try_parse(value: str) -> datetime:
    for fmt in _FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime from string: {value!r}")


class DateTimeConverter(Converter):
    """Normalize various datetime representations to :class:`~datetime.datetime`.

    Handles:
    - ISO 8601 strings  (``"2026-03-25T14:30:00"``)
    - Unix timestamps   (``1742910600``, ``"1742910600"``)
    - Common date strings (``"2026-03-25"``, ``"25/03/2026"``)

    Examples
    --------
    >>> dtc = DateTimeConverter()
    >>> dtc.convert("2026-03-25")
    datetime.datetime(2026, 3, 25, 0, 0)
    >>> dtc.to_iso(1742910600)
    '2026-03-25T14:30:00+00:00'
    """

    def __init__(self) -> None:
        super().__init__("datetime")

    def convert(self, value: Union[str, int, float]) -> datetime:
        """Convert *value* to a :class:`~datetime.datetime` object."""
        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=timezone.utc)

        if isinstance(value, str):
            if _NUMERIC_RE.match(value):
                return datetime.fromtimestamp(float(value), tz=timezone.utc)
            return _try_parse(value)

        raise TypeError(f"Cannot convert type {type(value).__name__!r} to datetime")

    def to_iso(self, value: Union[str, int, float, datetime]) -> str:
        """Convert *value* to an ISO 8601 string."""
        dt = self.convert(value)  # type: ignore[arg-type]
        return dt.isoformat()

    def to_timestamp(self, value: Union[str, int, float, datetime]) -> float:
        """Convert *value* to a Unix timestamp (float)."""
        dt = self.convert(value)  # type: ignore[arg-type]
        # If naive datetime, assume UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
