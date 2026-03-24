"""22+ pytest tests for agent-converter."""

import pytest
from datetime import datetime, timezone

from agent_converter import (
    Converter,
    NumberConverter,
    ByteConverter,
    DateTimeConverter,
    ConverterChain,
)


# ---------------------------------------------------------------------------
# Converter base
# ---------------------------------------------------------------------------

class DoubleConverter(Converter):
    def convert(self, value):
        return value * 2


def test_base_name():
    c = DoubleConverter("double")
    assert c.name == "double"


def test_base_call_alias():
    c = DoubleConverter("double")
    assert c(5) == 10


def test_base_can_convert_default():
    c = DoubleConverter("double")
    assert c.can_convert("anything") is True


# ---------------------------------------------------------------------------
# NumberConverter
# ---------------------------------------------------------------------------

def test_number_plain_float():
    nc = NumberConverter()
    assert nc.convert(3.14) == 3.14


def test_number_plain_int():
    nc = NumberConverter()
    assert nc.convert(42) == 42.0


def test_number_k_suffix():
    nc = NumberConverter()
    assert nc.convert("1.5K") == 1500.0


def test_number_m_suffix():
    nc = NumberConverter()
    assert nc.convert("2M") == 2_000_000.0


def test_number_b_suffix():
    nc = NumberConverter()
    assert nc.convert("1B") == 1_000_000_000.0


def test_number_commas():
    nc = NumberConverter()
    assert nc.convert("1,234,567") == 1_234_567.0


def test_number_underscores():
    nc = NumberConverter()
    assert nc.convert("1_000_000") == 1_000_000.0


def test_number_invalid_raises():
    nc = NumberConverter()
    with pytest.raises(ValueError):
        nc.convert("not-a-number")


def test_number_can_convert_true():
    nc = NumberConverter()
    assert nc.can_convert("1.5K") is True


def test_number_can_convert_false():
    nc = NumberConverter()
    assert nc.can_convert("hello world") is False


# ---------------------------------------------------------------------------
# ByteConverter
# ---------------------------------------------------------------------------

def test_bytes_gb_to_bytes():
    bc = ByteConverter()
    assert bc.convert("1.5GB") == 1.5 * 1024 ** 3


def test_bytes_mb_to_bytes():
    bc = ByteConverter()
    assert bc.convert("512MB") == 512 * 1024 ** 2


def test_bytes_gb_to_mb():
    bc = ByteConverter(to_unit="MB")
    assert bc.convert("1.5GB") == pytest.approx(1536.0)


def test_bytes_numeric_input():
    bc = ByteConverter(to_unit="KB")
    assert bc.convert(1024) == pytest.approx(1.0)


def test_bytes_convert_to():
    bc = ByteConverter()
    assert bc.convert_to("1.5GB", "MB") == pytest.approx(1536.0)


def test_bytes_invalid_unit_raises():
    with pytest.raises(ValueError):
        ByteConverter(to_unit="ZB")


def test_bytes_kb_to_bytes():
    bc = ByteConverter()
    assert bc.convert("100KB") == pytest.approx(102400.0)


# ---------------------------------------------------------------------------
# DateTimeConverter
# ---------------------------------------------------------------------------

def test_datetime_iso_string():
    dtc = DateTimeConverter()
    dt = dtc.convert("2026-03-25")
    assert dt.year == 2026
    assert dt.month == 3
    assert dt.day == 25


def test_datetime_unix_int():
    dtc = DateTimeConverter()
    dt = dtc.convert(0)
    assert dt == datetime(1970, 1, 1, tzinfo=timezone.utc)


def test_datetime_unix_string():
    dtc = DateTimeConverter()
    dt = dtc.convert("0")
    assert dt == datetime(1970, 1, 1, tzinfo=timezone.utc)


def test_datetime_passthrough():
    dtc = DateTimeConverter()
    now = datetime.now(tz=timezone.utc)
    assert dtc.convert(now) is now


def test_datetime_to_iso():
    dtc = DateTimeConverter()
    result = dtc.to_iso(0)
    assert result.startswith("1970-01-01")


def test_datetime_to_timestamp():
    dtc = DateTimeConverter()
    ts = dtc.to_timestamp("1970-01-01T00:00:00+00:00")
    assert ts == pytest.approx(0.0)


def test_datetime_invalid_raises():
    dtc = DateTimeConverter()
    with pytest.raises((ValueError, TypeError)):
        dtc.convert([1, 2, 3])


# ---------------------------------------------------------------------------
# ConverterChain
# ---------------------------------------------------------------------------

def test_chain_single():
    chain = ConverterChain([NumberConverter()])
    assert chain.convert("1.5K") == 1500.0


def test_chain_add_fluent():
    chain = ConverterChain()
    chain.add(NumberConverter())
    assert len(chain) == 1


def test_chain_multiple():
    # Number string -> float -> bytes interpretation via ByteConverter
    # We'll chain: parse "1024" as number, then treat the float as bytes -> KB
    nc = NumberConverter()
    bc = ByteConverter(to_unit="KB")
    chain = ConverterChain([nc, bc])
    # "1024" -> 1024.0 (float) -> 1.0 KB
    result = chain.convert("1024")
    assert result == pytest.approx(1.0)


def test_chain_empty():
    chain = ConverterChain([])
    assert chain.convert("hello") == "hello"


def test_chain_call_alias():
    chain = ConverterChain([NumberConverter()])
    assert chain("2M") == 2_000_000.0
