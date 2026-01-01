# Tests

This directory contains comprehensive test suites for the Trendyol scraper project.

## Test Structure

- `test_models.py` - Tests for Product and DBProduct models
- `test_scraper.py` - Tests for ScraperABC class methods
- `test_processing.py` - Tests for processing utility functions
- `test_main.py` - Tests for FastAPI endpoints and extract_product_data function

## Running Tests

Install test dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_models.py
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Test Coverage

The test suite covers:
- Model validation and database operations
- Web scraping functionality
- API endpoint behavior
- Error handling and edge cases
- Health check and status verification
