"""NumberConverter — parses human-readable numbers from strings."""

import re
from typing import Union

from .base import Converter

_SUFFIX_MAP = {
    "k": 1_000,
    "m": 1_000_000,
    "b": 1_000_000_000,
    "t": 1_000_000_000_000,
}

_NUMBER_RE = re.compile(
    r"^\s*([+-]?)"              # optional sign
    r"([\d,_]+(?:\.\d+)?)"     # integer or decimal, commas/underscores allowed
    r"\s*([kmbt])?\s*$",        # optional suffix
    re.IGNORECASE,
)


class NumberConverter(Converter):
    """Parse numbers from strings including K/M/B suffixes, commas, and underscores.

    Examples
    --------
    >>> nc = NumberConverter()
    >>> nc.convert("1.5K")
    1500.0
    >>> nc.convert("2M")
    2000000.0
    >>> nc.convert("1,234,567")
    1234567.0
    >>> nc.convert("1_000_000")
    1000000.0
    """

    def __init__(self) -> None:
        super().__init__("number")

    def can_convert(self, value: object) -> bool:
        if isinstance(value, (int, float)):
            return True
        if not isinstance(value, str):
            return False
        return bool(_NUMBER_RE.match(value))

    def convert(self, value: Union[str, int, float]) -> float:
        """Convert *value* to a float.

        Parameters
        ----------
        value:
            A numeric string (with optional K/M/B/T suffix, commas, or
            underscores), or a plain ``int``/``float``.

        Returns
        -------
        float
        """
        if isinstance(value, (int, float)):
            return float(value)

        m = _NUMBER_RE.match(str(value))
        if m is None:
            raise ValueError(f"Cannot parse number from: {value!r}")

        sign_str, number_str, suffix = m.groups()
        # Strip commas and underscores
        number_str = number_str.replace(",", "").replace("_", "")
        result = float(sign_str + number_str)

        if suffix:
            multiplier = _SUFFIX_MAP.get(suffix.lower(), 1)
            result *= multiplier

        return result
