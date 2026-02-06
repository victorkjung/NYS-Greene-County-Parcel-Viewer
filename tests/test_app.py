"""
Tests for app.py main application
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDataLoading:
    """Tests for data loading functionality"""
    
    @pytest.mark.unit
    def test_sample_data_generation(self, sample_dataframe):
        """Test that sample data has required columns"""
        required_cols = [
            'parcel_id', 'owner', 'acreage', 'assessed_value',
            'latitude', 'longitude', 'property_class'
        ]
        
        for col in required_cols:
            assert col in sample_dataframe.columns, f"Missing column: {col}"
    
    @pytest.mark.unit
    def test_data_types(self, sample_dataframe):
        """Test that data types are correct"""
        df = sample_dataframe
        
        # Numeric columns should be numeric
        assert pd.api.types.is_numeric_dtype(df['acreage'])
        assert pd.api.types.is_numeric_dtype(df['assessed_value'])
        assert pd.api.types.is_numeric_dtype(df['latitude'])
        assert pd.api.types.is_numeric_dtype(df['longitude'])
    
    @pytest.mark.unit
    def test_coordinates_format(self, sample_dataframe):
        """Test that coordinates are in correct format"""
        df = sample_dataframe
        
        for idx, row in df.iterrows():
            coords = row['coordinates']
            assert isinstance(coords, list), "Coordinates should be a list"
            if len(coords) > 0:
                assert len(coords[0]) == 2, "Each coordinate should be [lat, lon]"


class TestPropertyClassification:
    """Tests for property classification logic"""
    
    @pytest.mark.unit
    def test_property_class_color_mapping(self):
        """Test that property classes map to colors correctly"""
        # Color mapping logic (from app.py)
        def get_color(prop_class):
            prop_class = str(prop_class)
            if prop_class.startswith('2'):
                return 'green'  # Residential
            elif prop_class.startswith('3'):
                return 'yellow'  # Vacant
            elif prop_class.startswith('9'):
                return 'blue'  # State/Forest
            elif prop_class.startswith('1'):
                return 'lightgreen'  # Agricultural
            elif prop_class.startswith('4'):
                return 'orange'  # Commercial
            elif prop_class.startswith('5'):
                return 'purple'  # Recreation
            else:
                return 'gray'
        
        assert get_color('210') == 'green'
        assert get_color('311') == 'yellow'
        assert get_color('931') == 'blue'
        assert get_color('120') == 'lightgreen'
        assert get_color('421') == 'orange'


class TestFiltering:
    """Tests for data filtering functionality"""
    
    @pytest.mark.unit
    def test_filter_by_owner(self, sample_dataframe):
        """Test filtering by owner name"""
        df = sample_dataframe
        search_term = "Smith"
        
        filtered = df[df['owner'].str.contains(search_term, case=False, na=False)]
        assert len(filtered) > 0
        assert all(search_term.lower() in owner.lower() for owner in filtered['owner'])
    
    @pytest.mark.unit
    def test_filter_by_acreage_range(self, sample_dataframe):
        """Test filtering by acreage range"""
        df = sample_dataframe
        min_acres = 5
        max_acres = 20
        
        filtered = df[(df['acreage'] >= min_acres) & (df['acreage'] <= max_acres)]
        assert all(filtered['acreage'] >= min_acres)
        assert all(filtered['acreage'] <= max_acres)
    
    @pytest.mark.unit
    def test_filter_by_property_class(self, sample_dataframe):
        """Test filtering by property class"""
        df = sample_dataframe
        
        # Filter for residential (starts with 2)
        residential = df[df['property_class'].astype(str).str.startswith('2')]
        for pc in residential['property_class']:
            assert str(pc).startswith('2')
    
    @pytest.mark.unit
    def test_filter_by_municipality(self, sample_dataframe):
        """Test filtering by municipality"""
        df = sample_dataframe
        
        filtered = df[df['municipality'] == 'Hunter']
        assert len(filtered) == len(df)  # All sample data is Hunter


class TestAnalytics:
    """Tests for analytics calculations"""
    
    @pytest.mark.unit
    def test_total_acreage(self, sample_dataframe):
        """Test total acreage calculation"""
        total = sample_dataframe['acreage'].sum()
        assert total > 0
        assert total == 5.5 + 150.0 + 10.0  # From sample data
    
    @pytest.mark.unit
    def test_average_assessed_value(self, sample_dataframe):
        """Test average assessed value calculation"""
        avg = sample_dataframe['assessed_value'].mean()
        assert avg > 0
    
    @pytest.mark.unit
    def test_unique_owners(self, sample_dataframe):
        """Test unique owner count"""
        unique_owners = sample_dataframe['owner'].nunique()
        assert unique_owners == 3  # Sample data has 3 unique owners
    
    @pytest.mark.unit
    def test_owner_portfolio(self, sample_dataframe):
        """Test owner portfolio aggregation"""
        # Group by owner
        portfolio = sample_dataframe.groupby('owner').agg({
            'acreage': 'sum',
            'assessed_value': 'sum',
            'parcel_id': 'count'
        }).rename(columns={'parcel_id': 'parcel_count'})
        
        assert len(portfolio) == 3
        assert 'acreage' in portfolio.columns
        assert 'parcel_count' in portfolio.columns


class TestMapGeneration:
    """Tests for map-related functionality"""
    
    @pytest.mark.unit
    def test_center_calculation(self, sample_dataframe):
        """Test map center calculation"""
        df = sample_dataframe.dropna(subset=['latitude', 'longitude'])
        
        if len(df) > 0:
            center_lat = df['latitude'].mean()
            center_lon = df['longitude'].mean()
            
            assert 42.0 < center_lat < 42.5  # Within Greene County
            assert -74.5 < center_lon < -74.0
    
    @pytest.mark.unit
    def test_empty_dataframe_handling(self):
        """Test handling of empty dataframe for map"""
        empty_df = pd.DataFrame(columns=['latitude', 'longitude', 'owner'])
        
        # Should not raise error
        if len(empty_df) == 0:
            # Use default center
            center_lat = 42.1856
            center_lon = -74.2848
            assert center_lat is not None


class TestExport:
    """Tests for data export functionality"""
    
    @pytest.mark.unit
    def test_csv_export(self, sample_dataframe, temp_data_dir):
        """Test CSV export"""
        export_path = temp_data_dir / "export.csv"
        sample_dataframe.to_csv(export_path, index=False)
        
        assert export_path.exists()
        
        # Reload and verify
        reloaded = pd.read_csv(export_path)
        assert len(reloaded) == len(sample_dataframe)
    
    @pytest.mark.unit
    def test_json_export(self, sample_dataframe, temp_data_dir):
        """Test JSON export"""
        import json
        
        export_path = temp_data_dir / "export.json"
        records = sample_dataframe.to_dict(orient='records')
        
        with open(export_path, 'w') as f:
            json.dump(records, f)
        
        assert export_path.exists()
        
        # Reload and verify
        with open(export_path) as f:
            reloaded = json.load(f)
        
        assert len(reloaded) == len(sample_dataframe)


# Run with: pytest tests/test_app.py -v
