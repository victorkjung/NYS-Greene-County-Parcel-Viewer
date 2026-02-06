# Contributing to Greene County Property Finder

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## 📜 Code of Conduct

Please be respectful and considerate of others. We want this project to be welcoming to all contributors.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/NYS-Greene-County-Property-Search.git
   cd NYS-Greene-County-Property-Search
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/victorkjung/NYS-Greene-County-Property-Search.git
   ```

## 💻 Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running the App

```bash
streamlit run app.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_fetcher.py -v

# Run only unit tests (skip integration)
pytest -m "not integration"
```

## 🔧 Making Changes

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Creating a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

## 🎨 Code Style

We follow Python best practices and PEP 8 guidelines.

### Formatting

We use **Black** for code formatting:

```bash
# Format all files
black .

# Check formatting without changes
black --check .
```

### Linting

We use **flake8** for linting:

```bash
flake8 . --max-line-length=120
```

### Type Hints

Please use type hints for function parameters and return values:

```python
def fetch_parcels(
    municipality: str,
    max_records: int = 1000
) -> pd.DataFrame:
    """
    Fetch parcel data from API.
    
    Args:
        municipality: Name of the municipality
        max_records: Maximum records to fetch
        
    Returns:
        DataFrame with parcel data
    """
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_center(df: pd.DataFrame) -> tuple:
    """
    Calculate the geographic center of parcels.
    
    Args:
        df: DataFrame with 'latitude' and 'longitude' columns
        
    Returns:
        Tuple of (center_lat, center_lon)
        
    Raises:
        ValueError: If DataFrame is empty
        
    Example:
        >>> df = pd.DataFrame({'latitude': [42.1, 42.2], 'longitude': [-74.1, -74.2]})
        >>> calculate_center(df)
        (42.15, -74.15)
    """
    ...
```

## 🧪 Testing

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_fetcher.py      # API fetcher tests
├── test_app.py          # Application tests
└── test_utils.py        # Utility tests
```

### Writing Tests

- Use descriptive test names: `test_fetch_returns_dataframe_with_required_columns`
- Use fixtures for shared setup
- Mark slow tests with `@pytest.mark.slow`
- Mark integration tests with `@pytest.mark.integration`

### Test Example

```python
import pytest
from greene_county_fetcher import get_record_count

class TestRecordCount:
    """Tests for get_record_count function"""
    
    @pytest.mark.integration
    def test_returns_positive_count(self):
        """API should return positive record count"""
        count = get_record_count()
        assert count > 0
    
    @pytest.mark.unit
    def test_handles_invalid_municipality(self):
        """Should return 0 for invalid municipality"""
        count = get_record_count("InvalidTown12345")
        assert count == 0
```

## 📤 Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add municipality filtering to data fetch

- Add get_available_municipalities() function
- Update fetch_all_parcels() with municipality parameter
- Add tests for municipality filtering

Closes #123
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Adding tests
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

### Pull Request Process

1. **Update your branch** with latest changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request** on GitHub

4. **Fill out the PR template**:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

5. **Wait for review** and address feedback

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Descriptive commit messages

## 🐛 Reporting Issues

### Bug Reports

Please include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs

### Feature Requests

Please include:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (optional)

### Issue Template

```markdown
## Description
[Clear description of the issue]

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Python version: 
- OS: 
- Browser (if applicable):

## Additional Context
[Any other relevant information]
```

## 🙏 Thank You!

Your contributions help make this project better for everyone. If you have any questions, feel free to open an issue or reach out.

---

*Happy coding! 🏔️*
