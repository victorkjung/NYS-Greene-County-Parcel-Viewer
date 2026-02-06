# README Additions for Greene County Property Finder

Add these sections to enhance your README.md:

## 📌 Badges (Add at top of README)

```markdown
# 🗺️ Greene County Property Finder

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-APP-NAME.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/victorkjung/NYS-Greene-County-Property-Search/actions/workflows/ci.yml/badge.svg)](https://github.com/victorkjung/NYS-Greene-County-Property-Search/actions/workflows/ci.yml)
[![Data Update](https://github.com/victorkjung/NYS-Greene-County-Property-Search/actions/workflows/update-data.yml/badge.svg)](https://github.com/victorkjung/NYS-Greene-County-Property-Search/actions/workflows/update-data.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 🏔️ OnXHunt-style property identification for the Catskill Mountains
```

## 🐳 Docker Section (Add after Quick Start)

```markdown
## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t greene-county-property-finder .

# Run container
docker run -d -p 8501:8501 -v $(pwd)/data:/app/data greene-county-property-finder
```

Access the app at http://localhost:8501
```

## 🔄 Automatic Data Updates (Add to Using Real Data section)

```markdown
### Automatic Updates via GitHub Actions

The repository includes a GitHub Action that automatically fetches fresh parcel data weekly:

- **Schedule**: Every Sunday at 6 AM UTC
- **Data**: Hunter/Lanesville area parcels
- **Storage**: Committed to the `data/` directory

To trigger a manual update:
1. Go to Actions tab
2. Select "Update Parcel Data"
3. Click "Run workflow"
```

## 🧪 Testing Section (Add near end)

```markdown
## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run only unit tests (fast)
pytest -m "not integration"

# Run integration tests (requires API)
pytest -m integration
```
```

## 🤝 Contributing Section (Add near end)

```markdown
## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit: `git commit -m 'feat: Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request
```

## 📊 API Reference Section (Optional - Add for developers)

```markdown
## 📊 API Reference

### Data Fetching

```python
from greene_county_fetcher import fetch_greene_county_data, get_record_count

# Get total parcel count
total = get_record_count()
print(f"Total parcels: {total:,}")

# Get count for specific municipality
hunter_count = get_record_count("Hunter")
print(f"Hunter parcels: {hunter_count:,}")

# Fetch data with progress callback
def progress(msg):
    print(msg)

df = fetch_greene_county_data(
    municipality="Hunter",
    max_records=5000,
    progress_callback=progress
)
```

### Configuration

```python
from utils.config import get_config

config = get_config()
print(config.GREENE_COUNTY_API_URL)
print(config.DEFAULT_MUNICIPALITY)
```
```
