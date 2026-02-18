"""
Data Loader for Greene County Property Finder
Utilities for loading real parcel data from official NYS/Greene County sources

VERSION 3.0 - CLEANUP:
- Removed sample data fallback
- Better error handling
- Clear error messages about data availability
"""

import requests
import json
import pandas as pd
import geopandas as gpd
from pathlib import Path
from constants import DEFAULT_DATA_FILE
from shapely.geometry import shape, mapping
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GreeneCountyParcelLoader:
    """
    Load parcel data from Greene County and NYS GIS sources.
    
    NOTE: Greene County parcel polygons are NOT available in the public NYS GIS API.
    Only the county boundary footprint is available.
    
    Alternative data sources to explore:
    - Contact Greene County Real Property directly
    - Use NYS Assessment Lookup (single parcel at a time)
    - Greene County GIS: gis.gcgovny.com
    """
    
    # NYS GIS REST Service endpoints
    NYS_PARCEL_SERVICE = "https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Tax_Parcels_Public/MapServer"
    
    # Layer IDs
    LAYER_PARCELS = 1  # Actual parcel polygons
    LAYER_FOOTPRINT = 0  # County boundaries only
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def check_data_availability(self) -> dict:
        """
        Check what counties are available in the public API.
        Returns dict with availability info.
        """
        try:
            # Check the footprint layer to see what counties have data
            url = f"{self.NYS_PARCEL_SERVICE}/{self.LAYER_FOOTPRINT}/query"
            params = {
                "where": "1=1",
                "outFields": "NAME,FIPS_CODE",
                "returnGeometry": "false",
                "f": "json"
            }
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            counties = []
            if 'features' in data:
                for f in data['features']:
                    counties.append(f['attributes'])
            
            # Check if Greene is in the public parcels (layer 1)
            url_parcels = f"{self.NYS_PARCEL_SERVICE}/{self.LAYER_PARCELS}/query"
            params_parcels = {
                "where": "COUNTY_NAME='GREENE'",
                "outFields": "COUNTY_NAME",
                "returnGeometry": "false",
                "resultRecordCount": 1,
                "f": "json"
            }
            
            try:
                response = requests.get(url_parcels, params=params_parcels, timeout=30)
                greene_available = 'features' in response.json() and len(response.json().get('features', [])) > 0
            except:
                greene_available = False
            
            return {
                "available": greene_available,
                "counties": counties,
                "message": "Greene County parcel data IS available in public API" if greene_available else "Greene County parcel data is NOT available in public API. Contact county directly."
            }
            
        except Exception as e:
            return {
                "available": False,
                "counties": [],
                "message": f"Error checking availability: {str(e)}"
            }
    
    def fetch_parcels(self, county: str = "GREENE", municipality: str = None, limit: int = 1000) -> pd.DataFrame:
        """
        Fetch parcel data from NYS GIS.
        
        NOTE: This will likely fail for Greene County since parcels aren't in the public API.
        """
        url = f"{self.NYS_PARCEL_SERVICE}/{self.LAYER_PARCELS}/query"
        
        where_clause = f"COUNTY_NAME='{county.upper()}'"
        if municipality:
            where_clause += f" AND (MUNI_NAME='{municipality}' OR CITYTOWN_NAME='{municipality}')"
        
        params = {
            "where": where_clause,
            "outFields": "*",
            "returnGeometry": "true",
            "resultRecordCount": limit,
            "f": "json"
        }
        
        try:
            logger.info(f"Fetching parcels for {county}...")
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                raise Exception(f"API Error: {data['error'].get('message', 'Unknown error')}")
            
            if 'features' not in data or len(data['features']) == 0:
                raise Exception(f"No parcels found for {county}. Greene County parcel data is not available in the public NYS GIS API.")
            
            # Process features into DataFrame
            records = []
            for feature in data['features']:
                props = feature['attributes']
                record = {
                    'parcel_id': props.get('PRINT_KEY', ''),
                    'sbl': props.get('SBL', ''),
                    'owner': props.get('OWNER_NAME1', props.get('PRIMARY_OWNER', '')),
                    'mailing_address': props.get('MAIL_ADDR', ''),
                    'property_class': props.get('PROP_CLASS', ''),
                    'assessed_value': props.get('TOTAL_AV', 0),
                    'land_value': props.get('LAND_AV', 0),
                    'acreage': props.get('ACRES', 0),
                    'municipality': props.get('MUNI_NAME', props.get('CITYTOWN_NAME', '')),
                    'address': props.get('PARCEL_ADDR', ''),
                }
                records.append(record)
            
            return pd.DataFrame(records)
            
        except requests.RequestException as e:
            raise Exception(f"Network error fetching parcels: {str(e)}")
    
    def fetch_assessment_lookup(self, x: float, y: float) -> dict:
        """
        Use NYS Assessment Lookup to get parcel data for a specific coordinate.
        This works for any location in NYS!
        """
        url = "https://gisservices.its.ny.gov/arcgis/rest/services/NYSTaxAssessmentLookup/GPServer/TaxAssessment/execute"
        
        params = {
            "X": str(x),
            "Y": str(y),
            "f": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data and len(data['results']) > 0:
                return data['results'][0]['value']
            return {}
            
        except Exception as e:
            logger.error(f"Assessment lookup error: {e}")
            return {}
    
    def load_local_data(self, filename: str = None) -> pd.DataFrame:
        """Load previously downloaded/parced data from local files."""
        filename = filename or DEFAULT_DATA_FILE
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Local data file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return pd.DataFrame(data)


def get_sample_data() -> pd.DataFrame:
    """
    DEPRECATED: Sample data removed.
    Use fetch_parcels() or fetch_assessment_lookup() instead.
    """
    raise NotImplementedError(
        "Sample data has been removed. "
        " Greene County parcel data is not available in the public NYS GIS API. "
        " Options: 1) Contact Greene County directly, 2) Use Assessment Lookup for single parcels, "
        "3) Use a different county that's available in the API"
    )


if __name__ == "__main__":
    # Test availability
    loader = GreeneCountyParcelLoader()
    status = loader.check_data_availability()
    print(f" Greene County available: {status['available']}")
    print(f"Message: {status['message']}")
