# Double Sight Server

FastAPI backend for shot tracking and trend analysis.

## Development

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

## Testing

```bash
pytest
```

## Linting

```bash
ruff check src tests
ruff format src tests
pyright
```

