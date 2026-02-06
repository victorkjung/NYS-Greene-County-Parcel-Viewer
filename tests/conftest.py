"""
Pytest configuration and shared fixtures
"""

import pytest
import pandas as pd
import json
from pathlib import Path
import tempfile
import shutil


@pytest.fixture(scope="session")
def temp_data_dir():
    """Create a temporary data directory for tests"""
    temp_dir = tempfile.mkdtemp(prefix="test_data_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_parcel_data():
    """Sample parcel data for testing"""
    return [
        {
            "parcel_id": "86.1-1-1",
            "sbl": "86.00-1-1.000",
            "owner": "Smith, John",
            "mailing_address": "123 Main St",
            "mailing_city": "Lanesville",
            "mailing_state": "NY",
            "mailing_zip": "12450",
            "property_class": "210",
            "property_class_desc": "One Family Residential",
            "acreage": 5.5,
            "assessed_value": 250000,
            "land_value": 50000,
            "improvement_value": 200000,
            "municipality": "Hunter",
            "county": "Greene",
            "school_district": "Hunter-Tannersville",
            "latitude": 42.1856,
            "longitude": -74.2848,
            "coordinates": [[42.185, -74.284], [42.186, -74.284], [42.186, -74.285], [42.185, -74.285]],
            "annual_taxes": 6250.00,
            "tax_year": 2024
        },
        {
            "parcel_id": "86.1-1-2",
            "sbl": "86.00-1-2.000",
            "owner": "NYS DEC",
            "mailing_address": "625 Broadway",
            "mailing_city": "Albany",
            "mailing_state": "NY",
            "mailing_zip": "12233",
            "property_class": "931",
            "property_class_desc": "State Owned - Forest",
            "acreage": 150.0,
            "assessed_value": 500000,
            "land_value": 500000,
            "improvement_value": 0,
            "municipality": "Hunter",
            "county": "Greene",
            "school_district": "Hunter-Tannersville",
            "latitude": 42.1900,
            "longitude": -74.2900,
            "coordinates": [[42.189, -74.289], [42.191, -74.289], [42.191, -74.291], [42.189, -74.291]],
            "annual_taxes": 0,
            "tax_year": 2024
        },
        {
            "parcel_id": "86.1-1-3",
            "sbl": "86.00-1-3.000",
            "owner": "Mountain View LLC",
            "mailing_address": "456 Park Ave",
            "mailing_city": "New York",
            "mailing_state": "NY",
            "mailing_zip": "10022",
            "property_class": "311",
            "property_class_desc": "Vacant Land - Residential",
            "acreage": 10.0,
            "assessed_value": 75000,
            "land_value": 75000,
            "improvement_value": 0,
            "municipality": "Hunter",
            "county": "Greene",
            "school_district": "Hunter-Tannersville",
            "latitude": 42.1800,
            "longitude": -74.2800,
            "coordinates": [[42.179, -74.279], [42.181, -74.279], [42.181, -74.281], [42.179, -74.281]],
            "annual_taxes": 1875.00,
            "tax_year": 2024
        }
    ]


@pytest.fixture
def sample_dataframe(sample_parcel_data):
    """Sample DataFrame for testing"""
    return pd.DataFrame(sample_parcel_data)


@pytest.fixture
def sample_json_file(temp_data_dir, sample_parcel_data):
    """Create a sample JSON file with parcel data"""
    file_path = temp_data_dir / "test_parcels.json"
    with open(file_path, "w") as f:
        json.dump(sample_parcel_data, f)
    return file_path


@pytest.fixture
def mock_api_response():
    """Mock API response from Greene County ArcGIS"""
    return {
        "features": [
            {
                "attributes": {
                    "OBJECTID": 1,
                    "PRINT_KEY": "86.1-1-1",
                    "SBL": "86.00-1-1.000",
                    "OWNER": "Smith, John",
                    "MAIL_ADDR": "123 Main St",
                    "MAIL_CITY": "Lanesville",
                    "MAIL_STATE": "NY",
                    "MAIL_ZIP": "12450",
                    "PROP_CLASS": "210",
                    "ACRES": 5.5,
                    "TOTAL_AV": 250000,
                    "LAND_AV": 50000,
                    "MUNI_NAME": "Hunter"
                },
                "geometry": {
                    "rings": [[
                        [-74.284, 42.185],
                        [-74.284, 42.186],
                        [-74.285, 42.186],
                        [-74.285, 42.185],
                        [-74.284, 42.185]
                    ]]
                }
            }
        ]
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests that require API access"
    )
    config.addinivalue_line(
        "markers", "unit: marks unit tests"
    )
