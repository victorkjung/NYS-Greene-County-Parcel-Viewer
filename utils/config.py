"""
Configuration management for Greene County Property Finder

Loads configuration from environment variables and .env files

Usage:
    from utils.config import get_config
    
    config = get_config()
    print(config.GREENE_COUNTY_API_URL)
    print(config.DEFAULT_MUNICIPALITY)
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List
import json


def load_dotenv(env_file: Path = Path(".env")) -> dict:
    """
    Load environment variables from .env file
    
    Args:
        env_file: Path to .env file
        
    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse key=value
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    env_vars[key] = value
    
    return env_vars


@dataclass
class Config:
    """Application configuration"""
    
    # API Configuration
    GREENE_COUNTY_API_URL: str = "https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/arcgis/rest/services/Greene_County_Tax_Parcels/FeatureServer/0"
    BATCH_SIZE: int = 1000
    REQUEST_TIMEOUT: int = 60
    MAX_REQUESTS_PER_MINUTE: int = 30
    
    # Default Settings
    DEFAULT_MUNICIPALITY: str = "Hunter"
    DEFAULT_MAP_STYLE: str = "satellite"
    SHOW_LABELS_DEFAULT: bool = False
    DEFAULT_SAMPLE_PARCELS: int = 500
    
    # Cache Settings
    CACHE_EXPIRY_DAYS: int = 7
    CACHE_DIR: str = "data"
    AUTO_REFRESH_CACHE: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = False
    LOG_FILE_PATH: str = "logs/app.log"
    
    # Feature Flags
    ENABLE_API_FETCH: bool = True
    ENABLE_ANALYTICS: bool = True
    ENABLE_EXPORT: bool = True
    ENABLE_DRAWING_TOOLS: bool = True
    
    # Map Settings
    DEFAULT_LAT: float = 42.1856
    DEFAULT_LON: float = -74.2848
    DEFAULT_ZOOM: int = 14
    MAX_MAP_PARCELS: int = 5000
    
    @classmethod
    def from_env(cls, env_file: Optional[Path] = None) -> "Config":
        """
        Create Config from environment variables
        
        Args:
            env_file: Optional path to .env file
            
        Returns:
            Config instance
        """
        # Load .env file if provided
        if env_file:
            dotenv_vars = load_dotenv(env_file)
            for key, value in dotenv_vars.items():
                os.environ.setdefault(key, value)
        else:
            # Try to load from default locations
            for path in [Path(".env"), Path("../.env")]:
                if path.exists():
                    dotenv_vars = load_dotenv(path)
                    for key, value in dotenv_vars.items():
                        os.environ.setdefault(key, value)
                    break
        
        # Build config from environment
        return cls(
            GREENE_COUNTY_API_URL=os.environ.get("GREENE_COUNTY_API_URL", cls.GREENE_COUNTY_API_URL),
            BATCH_SIZE=int(os.environ.get("BATCH_SIZE", cls.BATCH_SIZE)),
            REQUEST_TIMEOUT=int(os.environ.get("REQUEST_TIMEOUT", cls.REQUEST_TIMEOUT)),
            MAX_REQUESTS_PER_MINUTE=int(os.environ.get("MAX_REQUESTS_PER_MINUTE", cls.MAX_REQUESTS_PER_MINUTE)),
            
            DEFAULT_MUNICIPALITY=os.environ.get("DEFAULT_MUNICIPALITY", cls.DEFAULT_MUNICIPALITY),
            DEFAULT_MAP_STYLE=os.environ.get("DEFAULT_MAP_STYLE", cls.DEFAULT_MAP_STYLE),
            SHOW_LABELS_DEFAULT=os.environ.get("SHOW_LABELS_DEFAULT", "false").lower() == "true",
            DEFAULT_SAMPLE_PARCELS=int(os.environ.get("DEFAULT_SAMPLE_PARCELS", cls.DEFAULT_SAMPLE_PARCELS)),
            
            CACHE_EXPIRY_DAYS=int(os.environ.get("CACHE_EXPIRY_DAYS", cls.CACHE_EXPIRY_DAYS)),
            CACHE_DIR=os.environ.get("CACHE_DIR", cls.CACHE_DIR),
            AUTO_REFRESH_CACHE=os.environ.get("AUTO_REFRESH_CACHE", "false").lower() == "true",
            
            LOG_LEVEL=os.environ.get("LOG_LEVEL", cls.LOG_LEVEL),
            LOG_TO_FILE=os.environ.get("LOG_TO_FILE", "false").lower() == "true",
            LOG_FILE_PATH=os.environ.get("LOG_FILE_PATH", cls.LOG_FILE_PATH),
            
            ENABLE_API_FETCH=os.environ.get("ENABLE_API_FETCH", "true").lower() == "true",
            ENABLE_ANALYTICS=os.environ.get("ENABLE_ANALYTICS", "true").lower() == "true",
            ENABLE_EXPORT=os.environ.get("ENABLE_EXPORT", "true").lower() == "true",
            ENABLE_DRAWING_TOOLS=os.environ.get("ENABLE_DRAWING_TOOLS", "true").lower() == "true",
            
            DEFAULT_LAT=float(os.environ.get("DEFAULT_LAT", cls.DEFAULT_LAT)),
            DEFAULT_LON=float(os.environ.get("DEFAULT_LON", cls.DEFAULT_LON)),
            DEFAULT_ZOOM=int(os.environ.get("DEFAULT_ZOOM", cls.DEFAULT_ZOOM)),
            MAX_MAP_PARCELS=int(os.environ.get("MAX_MAP_PARCELS", cls.MAX_MAP_PARCELS)),
        )
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            field: getattr(self, field)
            for field in self.__dataclass_fields__
        }
    
    def to_json(self) -> str:
        """Convert config to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def validate(self) -> List[str]:
        """
        Validate configuration
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if self.BATCH_SIZE < 100 or self.BATCH_SIZE > 5000:
            errors.append(f"BATCH_SIZE should be between 100 and 5000, got {self.BATCH_SIZE}")
        
        if self.REQUEST_TIMEOUT < 10:
            errors.append(f"REQUEST_TIMEOUT should be at least 10 seconds, got {self.REQUEST_TIMEOUT}")
        
        if not self.GREENE_COUNTY_API_URL.startswith("http"):
            errors.append(f"GREENE_COUNTY_API_URL should be a valid URL")
        
        if self.DEFAULT_LAT < 40 or self.DEFAULT_LAT > 45:
            errors.append(f"DEFAULT_LAT should be in NY range (40-45), got {self.DEFAULT_LAT}")
        
        if self.DEFAULT_LON < -80 or self.DEFAULT_LON > -70:
            errors.append(f"DEFAULT_LON should be in NY range (-80 to -70), got {self.DEFAULT_LON}")
        
        return errors


# Singleton config instance
_config: Optional[Config] = None


def get_config(reload: bool = False) -> Config:
    """
    Get the application configuration (singleton)
    
    Args:
        reload: Force reload configuration
        
    Returns:
        Config instance
    """
    global _config
    
    if _config is None or reload:
        _config = Config.from_env()
    
    return _config


# Example usage
if __name__ == "__main__":
    config = get_config()
    
    print("Configuration:")
    print("=" * 50)
    print(config.to_json())
    
    print("\nValidation:")
    errors = config.validate()
    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print("  ✅ All configuration valid")
