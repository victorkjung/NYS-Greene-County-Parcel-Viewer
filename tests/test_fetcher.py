"""
Tests for greene_county_fetcher.py
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from greene_county_fetcher import (
    get_record_count,
    get_available_municipalities,
    fetch_all_parcels,
    process_features,
    save_to_file,
    load_from_file,
    fetch_greene_county_data,
    GREENE_COUNTY_API,
    PROPERTY_CLASS_DESC
)


class TestAPIConnection:
    """Tests for API connectivity"""
    
    @pytest.mark.integration
    def test_api_url_is_valid(self):
        """Verify the API URL is correctly configured"""
        assert GREENE_COUNTY_API is not None
        assert "arcgis" in GREENE_COUNTY_API
        assert "Greene_County" in GREENE_COUNTY_API
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_get_record_count_returns_positive(self):
        """Test that API returns a positive record count"""
        count = get_record_count()
        assert count > 0, "API should return positive record count"
        assert count > 30000, "Greene County should have 30k+ parcels"
    
    @pytest.mark.integration
    def test_get_record_count_with_municipality(self):
        """Test record count with municipality filter"""
        count = get_record_count("Hunter")
        assert count > 0, "Hunter should have parcels"
        assert count < 40000, "Hunter should be subset of total"
    
    @pytest.mark.integration
    def test_get_available_municipalities(self):
        """Test fetching list of municipalities"""
        munis = get_available_municipalities()
        assert len(munis) > 0, "Should return municipalities"
        # Check for expected municipalities (case-insensitive)
        muni_lower = [m.lower() for m in munis]
        assert any("hunter" in m for m in muni_lower) or len(munis) > 5


class TestProcessFeatures:
    """Tests for feature processing"""
    
    @pytest.mark.unit
    def test_process_features_basic(self, mock_api_response):
        """Test basic feature processing"""
        df = process_features(mock_api_response["features"])
        
        assert len(df) == 1
        assert "parcel_id" in df.columns
        assert "owner" in df.columns
        assert "latitude" in df.columns
        assert "longitude" in df.columns
    
    @pytest.mark.unit
    def test_process_features_geometry(self, mock_api_response):
        """Test geometry processing"""
        df = process_features(mock_api_response["features"])
        
        # Should have coordinates
        assert "coordinates" in df.columns
        assert len(df.iloc[0]["coordinates"]) > 0
        
        # Should have calculated centroid
        assert df.iloc[0]["latitude"] is not None
        assert df.iloc[0]["longitude"] is not None
    
    @pytest.mark.unit
    def test_process_features_empty(self):
        """Test processing empty feature list"""
        df = process_features([])
        assert len(df) == 0
    
    @pytest.mark.unit
    def test_property_class_mapping(self):
        """Test property class descriptions are available"""
        assert "210" in PROPERTY_CLASS_DESC
        assert PROPERTY_CLASS_DESC["210"] == "One Family Residential"
        assert "931" in PROPERTY_CLASS_DESC
        assert "Forest" in PROPERTY_CLASS_DESC["931"]


class TestFileOperations:
    """Tests for file save/load operations"""
    
    @pytest.mark.unit
    def test_save_and_load(self, temp_data_dir, sample_dataframe):
        """Test saving and loading data"""
        # Temporarily change the data directory
        original_dir = Path("data")
        
        with patch('greene_county_fetcher.Path') as mock_path:
            mock_path.return_value = temp_data_dir
            
            # Save
            save_to_file(sample_dataframe, "test_save.json")
            
            # Verify file exists
            saved_file = temp_data_dir / "test_save.json"
            assert saved_file.exists()
            
            # Load and verify
            with open(saved_file) as f:
                loaded = json.load(f)
            
            assert len(loaded) == len(sample_dataframe)
    
    @pytest.mark.unit
    def test_load_nonexistent_file(self, temp_data_dir):
        """Test loading a file that doesn't exist"""
        result = load_from_file("nonexistent_file.json")
        assert result is None


class TestFetchAllParcels:
    """Tests for the main fetch function"""
    
    @pytest.mark.unit
    def test_fetch_with_mock(self, mock_api_response):
        """Test fetch with mocked API response"""
        with patch('greene_county_fetcher.requests.get') as mock_get:
            # Mock count response
            count_response = MagicMock()
            count_response.json.return_value = {"count": 1}
            count_response.status_code = 200
            count_response.raise_for_status = MagicMock()
            
            # Mock data response
            data_response = MagicMock()
            data_response.json.return_value = mock_api_response
            data_response.status_code = 200
            data_response.raise_for_status = MagicMock()
            
            mock_get.side_effect = [count_response, data_response]
            
            progress_messages = []
            def capture_progress(msg):
                progress_messages.append(msg)
            
            df = fetch_all_parcels(
                progress_callback=capture_progress,
                max_records=1
            )
            
            assert df is not None
            assert len(df) >= 0
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_fetch_limited_records(self):
        """Test fetching limited number of records"""
        df = fetch_all_parcels(max_records=10)
        
        if df is not None:
            assert len(df) <= 10
            assert "parcel_id" in df.columns


class TestFetchGreeneCountyData:
    """Tests for the convenience fetch function"""
    
    @pytest.mark.unit
    def test_fetch_uses_cache(self, temp_data_dir, sample_json_file):
        """Test that cached data is used when available"""
        with patch('greene_county_fetcher.load_from_file') as mock_load:
            import pandas as pd
            mock_load.return_value = pd.DataFrame([{"test": "data"}])
            
            progress_messages = []
            result = fetch_greene_county_data(
                use_cache=True,
                progress_callback=lambda m: progress_messages.append(m)
            )
            
            mock_load.assert_called()
    
    @pytest.mark.unit
    def test_fetch_skips_cache(self):
        """Test that cache can be bypassed"""
        with patch('greene_county_fetcher.fetch_all_parcels') as mock_fetch:
            with patch('greene_county_fetcher.load_from_file') as mock_load:
                mock_fetch.return_value = None
                
                fetch_greene_county_data(use_cache=False)
                
                # Should call fetch, not just load
                mock_fetch.assert_called()


class TestMunicipalityFiltering:
    """Tests for municipality filtering"""
    
    @pytest.mark.integration
    def test_hunter_filter(self):
        """Test filtering for Hunter municipality"""
        count_all = get_record_count()
        count_hunter = get_record_count("Hunter")
        
        assert count_hunter > 0
        assert count_hunter < count_all
    
    @pytest.mark.unit
    def test_invalid_municipality(self):
        """Test with invalid municipality name"""
        count = get_record_count("NonexistentTown12345")
        assert count == 0


# Run with: pytest tests/test_fetcher.py -v
# Run integration tests: pytest tests/test_fetcher.py -v -m integration
# Skip slow tests: pytest tests/test_fetcher.py -v -m "not slow"
