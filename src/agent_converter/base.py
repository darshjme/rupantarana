"""Base Converter interface."""

from abc import ABC, abstractmethod
from typing import Any


class Converter(ABC):
    """Abstract base class for all converters."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def convert(self, value: Any) -> Any:
        """Convert value to the target type/unit."""

    def can_convert(self, value: Any) -> bool:
        """Return True if this converter can handle the given value."""
        return True

    def __call__(self, value: Any) -> Any:
        """Alias for convert()."""
        return self.convert(value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
