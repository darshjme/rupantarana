# Contributing to agent-converter

Thank you for your interest in contributing! This document outlines the process.

## Getting Started

1. Fork the repository and clone locally.
2. Create a virtual environment and install dev dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. Run the test suite to make sure everything passes:
   ```bash
   python -m pytest tests/ -v
   ```

## Development Guidelines

- **Zero dependencies** — the library must remain dependency-free at runtime.
  Use only the Python standard library (`re`, `datetime`, `abc`, etc.).
- **Type hints** — all public methods must include type annotations.
- **Docstrings** — every public class and method needs a docstring.
- **Tests** — new features require tests. Bug fixes should include a regression test.

## Adding a Converter

1. Create `src/agent_converter/<your_name>.py`.
2. Subclass `Converter` and implement `convert()`.
3. Export it in `src/agent_converter/__init__.py`.
4. Add tests in `tests/test_converters.py`.

## Pull Request Process

1. Branch from `main` with a descriptive name (`feat/temperature-converter`).
2. Keep commits small and focused.
3. Update `CHANGELOG.md` under `[Unreleased]`.
4. Ensure `python -m pytest tests/ -v` passes with no failures.
5. Open a PR with a clear description of the change and why it's needed.

## Code of Conduct

Please read `CODE_OF_CONDUCT.md` before participating.
