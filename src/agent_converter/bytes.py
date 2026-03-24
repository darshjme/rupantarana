"""ByteConverter — converts between byte units."""

import re
from typing import Union

from .base import Converter

_UNIT_BYTES = {
    "bytes": 1,
    "byte": 1,
    "b": 1,
    "kb": 1_024,
    "mb": 1_024 ** 2,
    "gb": 1_024 ** 3,
    "tb": 1_024 ** 4,
    "pb": 1_024 ** 5,
}

_BYTE_RE = re.compile(
    r"^\s*([+-]?[\d,_]+(?:\.\d+)?)\s*([a-zA-Z]+)?\s*$"
)


def _parse_bytes(value: Union[str, int, float]) -> float:
    """Return the number of bytes represented by *value*."""
    if isinstance(value, (int, float)):
        return float(value)

    m = _BYTE_RE.match(str(value))
    if m is None:
        raise ValueError(f"Cannot parse byte value from: {value!r}")

    num_str, unit_str = m.groups()
    num = float(num_str.replace(",", "").replace("_", ""))
    unit = (unit_str or "bytes").lower()

    factor = _UNIT_BYTES.get(unit)
    if factor is None:
        raise ValueError(f"Unknown byte unit: {unit_str!r}")

    return num * factor


class ByteConverter(Converter):
    """Convert between byte units.

    Parameters
    ----------
    to_unit:
        Target unit for :py:meth:`convert`.  One of
        ``bytes``, ``KB``, ``MB``, ``GB``, ``TB``.

    Examples
    --------
    >>> bc = ByteConverter()
    >>> bc.convert("1.5GB")
    1610612736.0
    >>> ByteConverter(to_unit="MB").convert("1.5GB")
    1536.0
    >>> bc.convert_to("1.5GB", "MB")
    1536.0
    """

    def __init__(self, to_unit: str = "bytes") -> None:
        super().__init__("bytes")
        self._to_unit = to_unit.lower()
        if self._to_unit not in _UNIT_BYTES:
            raise ValueError(f"Unknown target unit: {to_unit!r}")

    @property
    def to_unit(self) -> str:
        return self._to_unit

    def convert(self, value: Union[str, int, float]) -> float:
        """Convert *value* to :attr:`to_unit`."""
        raw_bytes = _parse_bytes(value)
        return raw_bytes / _UNIT_BYTES[self._to_unit]

    def convert_to(self, value: Union[str, int, float], unit: str) -> float:
        """Convert *value* to an arbitrary *unit* on-the-fly."""
        raw_bytes = _parse_bytes(value)
        unit_lower = unit.lower()
        factor = _UNIT_BYTES.get(unit_lower)
        if factor is None:
            raise ValueError(f"Unknown byte unit: {unit!r}")
        return raw_bytes / factor
