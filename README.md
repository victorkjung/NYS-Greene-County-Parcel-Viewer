# 🗺️ Greene County Property Finder

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **OnXHunt-style** property owner identification application for Greene County, NY (Catskill Mountains region)

![Property Finder](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## ✨ Features

### 🗺️ Interactive Property Map
- **Multiple base maps** - Satellite, Topographic, Street, Dark mode
- **Color-coded parcels** by property type
- **Click-to-view** owner info, assessed values, tax data
- **Drawing tools** for marking areas of interest
- **GPS location** support

### 🔍 Advanced Search & Filter
- Search by **owner name**, **parcel ID**, or **address**
- Filter by **property type**, **acreage**, **assessed value**
- Filter by **municipality** or **zip code**

### 📊 Analytics Dashboard
- Property type distribution charts
- Top landowners by acreage and value
- Tax revenue analysis
- Local vs non-local owner breakdown

### 👤 Owner Lookup
- View all parcels owned by a specific owner
- Portfolio analysis with totals
- Export owner data (CSV/JSON)

### 📥 Data Download
- Download parcels by zip code
- Multiple formats: CSV, JSON, GeoJSON
- Batch download for multiple areas

### 🔧 Data Management
- **Fetch real data** from Greene County ArcGIS
- Download all 38,000+ parcels or filter by municipality
- Upload custom datasets
- Automatic caching

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone or extract the repository
cd greene-county-property-finder

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📡 Fetching Real Data

The app can fetch actual parcel data from Greene County's official ArcGIS server:

### Option 1: Via the App (Easiest)
1. Open the app and go to **🔧 Data Management** page
2. Select coverage area:
   - **Hunter (Lanesville Area)** - ~2,000 parcels, fast
   - **All of Greene County** - ~38,000 parcels, slower
3. Click **🚀 Download** and wait
4. Data is automatically cached

### Option 2: Command Line
```bash
# Fetch Hunter/Lanesville area
python greene_county_fetcher.py --lanesville

# Fetch all of Greene County
python greene_county_fetcher.py

# List available municipalities
python greene_county_fetcher.py --list

# Fetch specific municipality
python greene_county_fetcher.py -m Windham
```

### Option 3: Python API
```python
from greene_county_fetcher import fetch_greene_county_data

# Fetch with progress updates
df = fetch_greene_county_data(
    municipality="Hunter",
    progress_callback=print
)
print(f"Fetched {len(df)} parcels")
```

---

## 📁 Project Structure

```
greene-county-property-finder/
├── app.py                      # Main Streamlit application
├── greene_county_fetcher.py    # Greene County API fetcher
├── data_loader.py              # Data loading utilities
├── nys_data_fetcher.py         # NYS GIS data fetcher
├── constants.py                # Application constants
├── ui.py                       # UI components
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
│
├── pages/                      # Streamlit pages
│   ├── 1_📊_Analytics.py
│   ├── 2_👤_Owner_Lookup.py
│   ├── 3_📥_Download_Data.py
│   └── 4_🔧_Data_Management.py
│
├── data/                       # Cached parcel data
│   └── .gitkeep
│
├── tests/                      # Test suite
│   ├── conftest.py
│   ├── test_fetcher.py
│   └── test_app.py
│
├── utils/                      # Utility modules
│   ├── logger.py
│   ├── cache.py
│   └── config.py
│
├── .github/workflows/          # CI/CD
│   ├── ci.yml
│   └── update-data.yml
│
├── .streamlit/config.toml      # Streamlit config
├── Dockerfile                  # Docker support
├── docker-compose.yml
├── Makefile                    # Dev commands
└── README.md
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Using Docker Directly
```bash
docker build -t property-finder .
docker run -d -p 8501:8501 -v $(pwd)/data:/app/data property-finder
```

Access at **http://localhost:8501**

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run only unit tests
pytest -m "not integration"
```

---

## 🔧 Development Commands

Using the Makefile:
```bash
make help          # Show all commands
make run           # Run the app
make test          # Run tests
make lint          # Check code quality
make format        # Format code
make fetch-data    # Fetch parcel data
make docker-run    # Run with Docker
```

---

## 📊 Data Fields

| Field | Description |
|-------|-------------|
| `parcel_id` | Unique parcel identifier |
| `sbl` | Section-Block-Lot number |
| `owner` | Property owner name |
| `mailing_address` | Owner mailing address |
| `property_class` | NYS property class code |
| `property_class_desc` | Class description |
| `acreage` | Parcel size in acres |
| `assessed_value` | Total assessed value |
| `land_value` | Land-only value |
| `improvement_value` | Improvements value |
| `municipality` | Town/city name |
| `school_district` | School district |
| `coordinates` | Parcel boundary |

---

## 🎨 Property Type Colors

| Color | Type |
|-------|------|
| 🟢 Green | Residential |
| 🟡 Yellow | Vacant Land |
| 🔵 Blue | State/Forest |
| 🟢 Light Green | Agricultural |
| 🟠 Orange | Commercial |
| 🟣 Purple | Recreation |
| ⚪ Gray | Other |

---

## 📮 Supported Zip Codes

| Zip | Location | Town |
|-----|----------|------|
| 12450 | Lanesville | Hunter |
| 12442 | Hunter | Hunter |
| 12485 | Tannersville | Hunter |
| 12434 | Haines Falls | Hunter |
| 12496 | Windham | Windham |
| 12414 | Catskill | Catskill |
| 12464 | Phoenicia | Shandaken |
| ... | [See constants.py for full list] |

---

## ⚖️ Legal Notice

**Property boundary data is for reference only.** Always verify with official county records before making decisions.

This application is not affiliated with Greene County or New York State.

---

## 🔗 Resources

- [Greene County GIS](https://www.greenegov.com/)
- [NYS GIS Clearinghouse](https://gis.ny.gov/)
- [NYS Real Property Tax](https://www.tax.ny.gov/research/property/)

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

*Built for property research in the beautiful Catskill Mountains* 🏔️
