# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-25

### Added
- `Converter` — abstract base class with `convert()`, `can_convert()`, and `__call__()`.
- `NumberConverter` — parses human-readable number strings (K/M/B/T suffixes, commas, underscores).
- `ByteConverter` — converts between byte units (bytes, KB, MB, GB, TB, PB) with `convert()` and `convert_to()`.
- `DateTimeConverter` — normalizes ISO 8601, Unix timestamps, and common date strings to `datetime` objects.
- `ConverterChain` — composable pipeline that applies converters in sequence.
- 22 pytest tests with 100 % pass rate.
- Zero runtime dependencies (uses only Python standard library: `re`, `datetime`, `abc`).
