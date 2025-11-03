# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Master's Program in Data Engineering with AI** - a comprehensive educational repository designed to take learners from beginner to expert level in Data Engineering. The project follows strict TDD (Test-Driven Development) and quality standards, with all code evaluated through a rigorous quality system before completion.

**Current Status:** 4/10 modules completed (40%), 13/31 projects completed (42%)

## Repository Structure

```
Curso-Data-Engineering/
├── modulo-01-fundamentos/           # ✅ Python, CSV, logging (100% complete)
├── modulo-02-sql/                   # 🔄 SQL básico e intermedio (33% complete)
├── modulo-03-ingenieria-datos/      # 🔄 ETL, Pandas, data quality (33% complete)
├── modulo-04-apis-scraping/         # ✅ APIs REST, scraping (100% complete)
├── modulo-05-bases-datos-avanzadas/ # 🔄 PostgreSQL, MongoDB (33% complete)
├── modulo-06-airflow/               # ⏳ Pipeline orchestration (pending)
├── documentacion/                   # Documentation, guides, reports
│   ├── jira/                        # Jira tickets (JAR-*)
│   ├── reportes/                    # Quality reports
│   ├── guias/                       # Installation & quality guides
│   └── juego/                       # Educational game files
├── scripts/                         # Utility scripts
├── .github/workflows/               # CI/CD pipelines
└── .cursor/                         # Cursor AI configuration
```

### Project Structure Pattern

Each topic follows this structure:
```
tema-X-nombre/
├── 01-TEORIA.md           # Theory (~3,500-4,500 words)
├── 02-EJEMPLOS.md         # Worked examples (4-5)
├── 03-EJERCICIOS.md       # Exercises (12-15)
└── 04-proyecto-practico/  # Practical project
    ├── README.md          # Project overview
    ├── ARQUITECTURA.md    # Architecture documentation
    ├── requirements.txt   # Python dependencies
    ├── src/               # Source code modules
    │   ├── __init__.py
    │   └── *.py           # Individual modules
    └── tests/             # Test suite
        ├── __init__.py
        ├── conftest.py    # Pytest fixtures
        └── test_*.py      # Unit tests
```

## Development Commands

### Setting Up Environment

```bash
# Verify Python version (must be 3.13+)
python --version

# Create virtual environment
python -m venv venv

# Activate environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Install dependencies for a specific module
cd modulo-XX-nombre/tema-Y-nombre/04-proyecto-practico
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests with coverage (from project root)
pytest --cov=src --cov-report=term-missing --cov-report=html -v

# Run tests for specific module
pytest tests/test_module.py -v

# Run with strict coverage requirement (80% minimum)
pytest --cov=src --cov-fail-under=80 -v

# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Then open: htmlcov/index.html
```

### Quality Check (Run Before Completion)

Every project must pass quality check before being marked complete:

```bash
# 1. Format code with Black
black src/ tests/

# 2. Check linting with flake8
flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503,C901

# 3. Sort imports
isort src/ tests/ --profile black

# 4. Type checking (optional but recommended)
mypy src/ --ignore-missing-imports

# 5. Run full test suite with coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=80 -v

# 6. Security scan (optional)
bandit -r src/ -c pyproject.toml
```

### Docker Services

```bash
# Start all services (PostgreSQL, MongoDB, Airflow, Redis)
docker-compose up -d

# View logs
docker-compose logs -f postgres
docker-compose logs -f airflow-webserver

# Stop services
docker-compose down

# Access PostgreSQL
docker exec -it master-postgres psql -U dataeng_user -d dataeng_db

# Access MongoDB
docker exec -it master-mongodb mongosh -u admin -p MongoAdmin2025!SecurePass

# Access Airflow Web UI
# http://localhost:8080 (admin / Airflow2025!Admin)
```

## Code Quality Standards

### Quality Evaluation System

All code is evaluated on a 0-10 scale across 8 categories before approval:

| Category | Weight | Minimum Standard |
|----------|--------|------------------|
| **Tests** | 25% | 100% passing, >80% coverage |
| **Type Hints** | 15% | 100% of functions typed |
| **Docstrings** | 15% | 100% with Args/Returns/Examples |
| **Architecture** | 15% | Functions <50 lines, DRY, KISS |
| **Error Handling** | 10% | Specific exceptions, validations |
| **Documentation** | 10% | README + CHANGELOG updated |
| **Security** | 5% | No credentials, validated inputs |
| **Pedagogy** | 5% | Logical progression, clear examples |

**Approval Criteria:**
- **9.5-10.0:** Excellent ✅ APPROVED WITH DISTINCTION
- **9.0-9.4:** Very Good ✅ APPROVED
- **8.0-8.9:** Good ✅ APPROVED
- **< 8.0:** ⚠️ REQUIRES IMPROVEMENTS

### TDD (Test-Driven Development)

This project follows strict TDD:
1. Write tests BEFORE implementing code
2. All tests must pass (100%)
3. Coverage target: >80% (ideally >90%)
4. Test categories: unit, integration, security

### Code Conventions

```python
# Functions and variables: snake_case
def calculate_average(numbers: list[float]) -> float:
    """Calculate arithmetic mean."""
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Classes: PascalCase
class DataValidator:
    pass

# No accents or spaces in names
# Good: def calcular_media()
# Bad: def calcular_média()
```

### Docstring Format (Required)

```python
def process_data(data: list[dict], filters: dict) -> list[dict]:
    """
    Process and filter data based on criteria.

    Args:
        data: List of dictionaries containing raw data
        filters: Dictionary with filter criteria
            - 'min_value': Minimum value threshold
            - 'max_value': Maximum value threshold

    Returns:
        Filtered list of dictionaries

    Raises:
        ValueError: If data is empty or filters are invalid
        TypeError: If data format is incorrect

    Example:
        >>> data = [{'value': 10}, {'value': 20}]
        >>> filters = {'min_value': 15}
        >>> process_data(data, filters)
        [{'value': 20}]
    """
    pass
```

### Import Organization

```python
# 1. Standard library
import os
import sys
from typing import Optional, List

# 2. Third-party packages
import pytest
import pandas as pd
from sqlalchemy import create_engine

# 3. Local modules
from src.validator import validate_data
from src.utils import clean_string
```

## Git Workflow (CRITICAL)

### ⛔ NEVER PUSH DIRECTLY TO MAIN

**Main branch is protected.** All changes MUST go through Pull Requests.

### Correct Workflow

```bash
# 1. Ensure you're on main and updated
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/descriptive-name
# or for this session: claude/init-project-011CUfWLKXjSpPNyp5C3pHqX

# 3. Make changes and commit
git add .
git commit -m "feat: descriptive message"

# 4. Push feature branch
git push -u origin feature/descriptive-name

# 5. Create Pull Request (never merge directly)
gh pr create --base main --title "..." --body "..."
```

### Commit Message Format (Conventional Commits)

```bash
feat: Add new data validation module
fix: Correct SQL injection vulnerability in queries
docs: Update installation guide
refactor: Simplify ETL pipeline logic
test: Add tests for edge cases in CSV parser
chore: Update dependencies
style: Format code with black
perf: Optimize database query performance
ci: Update GitHub Actions workflow
```

### Current Development Branch

**You are working on:** `claude/init-project-011CUfWLKXjSpPNyp5C3pHqX`

All changes for this session should be committed and pushed to this branch.

## Architecture Patterns

### Module Organization

Each project follows clean architecture:
- **Pure functions:** No side effects when possible
- **Context managers:** For database connections and file operations
- **Validation first:** Always validate inputs before processing
- **Explicit error handling:** Specific exception types with clear messages

### Example: Database Connection Pattern

```python
# Good: Context manager with explicit error handling
from contextlib import contextmanager
import sqlite3

@contextmanager
def get_connection(db_path: str):
    """Context manager for database connections."""
    if not db_path:
        raise ValueError("Database path cannot be empty")

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
```

### Example: Input Validation Pattern

```python
def validate_data(data: list[dict]) -> None:
    """
    Validate input data structure and content.

    Raises:
        ValueError: If data is empty or invalid
        TypeError: If data format is incorrect
    """
    if not data:
        raise ValueError("Data cannot be empty")

    if not isinstance(data, list):
        raise TypeError(f"Expected list, got {type(data).__name__}")

    for item in data:
        if not isinstance(item, dict):
            raise TypeError("All items must be dictionaries")
```

## Testing Patterns

### Fixture Organization (conftest.py)

```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    yield path
    os.close(fd)
    os.unlink(path)

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return [
        {"id": 1, "name": "Alice", "value": 100},
        {"id": 2, "name": "Bob", "value": 200},
    ]
```

### Test Structure

```python
def test_function_happy_path():
    """Test normal operation."""
    # Arrange
    data = [1, 2, 3]

    # Act
    result = calculate_average(data)

    # Assert
    assert result == 2.0

def test_function_edge_case():
    """Test edge case: single element."""
    result = calculate_average([5])
    assert result == 5.0

def test_function_error_handling():
    """Test error handling: empty list."""
    with pytest.raises(ValueError, match="cannot be empty"):
        calculate_average([])
```

## CI/CD Pipeline

### Automated Checks

The CI pipeline (.github/workflows/ci.yml) runs on every push and PR:

1. **Linting:** black, isort, flake8, mypy
2. **Tests:** Full test suite with coverage
3. **Security:** bandit, safety checks
4. **Build:** Package validation

All checks must pass before merging.

## Educational Game Integration

This repository includes an educational game (`documentacion/juego/`) that tracks student progress through missions that correspond to course modules. Game files are excluded from quality checks but should not be modified without explicit instruction.

## Documentation Requirements

When completing a new topic or module:

1. **Update documentacion/CHANGELOG.md** with changes
2. **Create/update README.md** in the project directory
3. **Document architecture** in ARQUITECTURA.md if applicable
4. **Generate quality report** following template in documentacion/jira/
5. **Update progress** in main README.md

## Security Practices

### Required Security Measures

- **SQL Injection Prevention:** Always use parameterized queries
- **Input Validation:** Validate all external inputs
- **Password Handling:** Use bcrypt/argon2 for hashing
- **Secrets Management:** Never commit credentials (use .env files)
- **Rate Limiting:** Implement for all API clients
- **HTTPS Only:** No plain HTTP connections

### Example: Safe SQL Query

```python
# Good: Parameterized query
def get_user(conn, user_id: int):
    cursor = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )
    return cursor.fetchone()

# Bad: String concatenation (SQL injection risk)
def get_user_unsafe(conn, user_id: int):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # ❌ NEVER DO THIS
    cursor = conn.execute(query)
    return cursor.fetchone()
```

## Common Pitfalls to Avoid

1. **Don't push to main directly** - Always use feature branches and PRs
2. **Don't skip tests** - Coverage must be >80%
3. **Don't omit type hints** - All functions must be typed
4. **Don't leave hardcoded credentials** - Use environment variables
5. **Don't create files in root** - Follow directory structure
6. **Don't modify .cursor/ or .github/** without explicit instruction
7. **Don't skip quality check** before marking tasks complete

## Performance Considerations

- Use generators for large datasets
- Implement caching where appropriate (e.g., API responses)
- Use async/await for I/O-bound operations
- Profile code before optimizing
- Document performance improvements with metrics

## Support Resources

- **Quality Guide:** documentacion/guias/GUIA_QUALITY_CHECK.md
- **Installation Guide:** documentacion/GUIA_INSTALACION.md
- **Full Program:** documentacion/PROGRAMA_MASTER.md
- **Changelog:** documentacion/CHANGELOG.md
- **Critical Rules:** REGLAS_CRITICAS_AGENTES.md
