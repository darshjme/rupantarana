"""ConverterChain — apply converters in sequence."""

from __future__ import annotations

from typing import Any

from .base import Converter


class ConverterChain(Converter):
    """Apply a list of converters in sequence.

    Each converter's output becomes the next converter's input.

    Parameters
    ----------
    converters:
        Ordered list of :class:`~agent_converter.Converter` instances.

    Examples
    --------
    >>> from agent_converter import NumberConverter, ByteConverter, ConverterChain
    >>> chain = ConverterChain([NumberConverter()])
    >>> chain.convert("1_000_000")
    1000000.0
    """

    def __init__(self, converters: list[Converter] | None = None) -> None:
        super().__init__("chain")
        self._converters: list[Converter] = list(converters or [])

    def add(self, converter: Converter) -> "ConverterChain":
        """Append *converter* to the chain and return *self* for fluent chaining."""
        self._converters.append(converter)
        return self

    def convert(self, value: Any) -> Any:
        """Pass *value* through each converter in order."""
        result = value
        for conv in self._converters:
            result = conv.convert(result)
        return result

    def __len__(self) -> int:
        return len(self._converters)

    def __repr__(self) -> str:
        return f"ConverterChain(converters={self._converters!r})"
