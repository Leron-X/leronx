# Contributing to LeronX Engine

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/Leron-X/leronx.git
cd leronx
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

We use `black` for formatting and `ruff` for linting:

```bash
black src/ tests/
ruff check src/ tests/
```

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
