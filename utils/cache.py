"""
File-based caching utilities for Greene County Property Finder

Usage:
    from utils.cache import file_cache
    
    @file_cache(expiry_hours=24)
    def fetch_expensive_data(param):
        # This result will be cached for 24 hours
        return expensive_api_call(param)
"""

import hashlib
import json
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional, Union
import os


# Default cache directory
CACHE_DIR = Path(os.environ.get("CACHE_DIR", "data/.cache"))


def get_cache_key(*args, **kwargs) -> str:
    """
    Generate a cache key from function arguments
    
    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        MD5 hash string
    """
    # Create a string representation of the arguments
    key_data = json.dumps([args, kwargs], sort_keys=True, default=str)
    return hashlib.md5(key_data.encode()).hexdigest()


def file_cache(
    expiry_hours: int = 24,
    cache_dir: Optional[Path] = None,
    use_pickle: bool = False
):
    """
    Decorator to cache function results to disk
    
    Args:
        expiry_hours: How long to keep cached results (in hours)
        cache_dir: Directory to store cache files
        use_pickle: Use pickle instead of JSON (for complex objects)
        
    Returns:
        Decorated function
        
    Example:
        @file_cache(expiry_hours=12)
        def fetch_data(municipality: str):
            return api_call(municipality)
    """
    cache_path = cache_dir or CACHE_DIR
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache directory
            cache_path.mkdir(parents=True, exist_ok=True)
            
            # Generate cache key
            key = get_cache_key(func.__name__, *args, **kwargs)
            ext = ".pkl" if use_pickle else ".json"
            cache_file = cache_path / f"{func.__name__}_{key}{ext}"
            
            # Check if cache exists and is valid
            if cache_file.exists():
                stat = cache_file.stat()
                age = datetime.now() - datetime.fromtimestamp(stat.st_mtime)
                
                if age < timedelta(hours=expiry_hours):
                    # Cache hit - load and return
                    try:
                        if use_pickle:
                            with open(cache_file, 'rb') as f:
                                return pickle.load(f)
                        else:
                            with open(cache_file, 'r') as f:
                                return json.load(f)
                    except (json.JSONDecodeError, pickle.PickleError):
                        # Cache corrupted, will regenerate
                        pass
            
            # Cache miss - execute function
            result = func(*args, **kwargs)
            
            # Save to cache
            try:
                if use_pickle:
                    with open(cache_file, 'wb') as f:
                        pickle.dump(result, f)
                else:
                    with open(cache_file, 'w') as f:
                        json.dump(result, f, default=str)
            except (TypeError, pickle.PickleError) as e:
                # If caching fails, just return the result
                print(f"Warning: Could not cache result: {e}")
            
            return result
        
        # Add cache control methods to the wrapper
        wrapper.clear_cache = lambda: clear_function_cache(func.__name__, cache_path)
        wrapper.cache_info = lambda: get_cache_info(func.__name__, cache_path)
        
        return wrapper
    
    return decorator


def clear_function_cache(func_name: str, cache_dir: Path = CACHE_DIR) -> int:
    """
    Clear cache files for a specific function
    
    Args:
        func_name: Name of the function
        cache_dir: Cache directory
        
    Returns:
        Number of files deleted
    """
    count = 0
    if cache_dir.exists():
        for cache_file in cache_dir.glob(f"{func_name}_*"):
            cache_file.unlink()
            count += 1
    return count


def clear_cache(cache_dir: Path = CACHE_DIR) -> int:
    """
    Clear all cache files
    
    Args:
        cache_dir: Cache directory
        
    Returns:
        Number of files deleted
    """
    count = 0
    if cache_dir.exists():
        for cache_file in cache_dir.glob("*"):
            if cache_file.is_file():
                cache_file.unlink()
                count += 1
    return count


def get_cache_info(func_name: Optional[str] = None, cache_dir: Path = CACHE_DIR) -> dict:
    """
    Get information about cached data
    
    Args:
        func_name: Optional function name to filter
        cache_dir: Cache directory
        
    Returns:
        Dictionary with cache statistics
    """
    info = {
        "cache_dir": str(cache_dir),
        "total_files": 0,
        "total_size_mb": 0,
        "files": []
    }
    
    if not cache_dir.exists():
        return info
    
    pattern = f"{func_name}_*" if func_name else "*"
    
    for cache_file in cache_dir.glob(pattern):
        if cache_file.is_file():
            stat = cache_file.stat()
            age = datetime.now() - datetime.fromtimestamp(stat.st_mtime)
            
            info["files"].append({
                "name": cache_file.name,
                "size_kb": stat.st_size / 1024,
                "age_hours": age.total_seconds() / 3600,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
            
            info["total_files"] += 1
            info["total_size_mb"] += stat.st_size / (1024 * 1024)
    
    return info


def cleanup_expired_cache(expiry_hours: int = 24, cache_dir: Path = CACHE_DIR) -> int:
    """
    Remove expired cache files
    
    Args:
        expiry_hours: Maximum age in hours
        cache_dir: Cache directory
        
    Returns:
        Number of files deleted
    """
    count = 0
    if cache_dir.exists():
        for cache_file in cache_dir.glob("*"):
            if cache_file.is_file():
                stat = cache_file.stat()
                age = datetime.now() - datetime.fromtimestamp(stat.st_mtime)
                
                if age > timedelta(hours=expiry_hours):
                    cache_file.unlink()
                    count += 1
    return count


class CacheManager:
    """
    Manager class for handling cached data
    
    Usage:
        cache = CacheManager()
        cache.set("my_key", {"data": "value"})
        data = cache.get("my_key")
    """
    
    def __init__(self, cache_dir: Path = CACHE_DIR, default_expiry_hours: int = 24):
        self.cache_dir = cache_dir
        self.default_expiry_hours = default_expiry_hours
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                # Check expiry
                if "_expires" in data:
                    expires = datetime.fromisoformat(data["_expires"])
                    if datetime.now() > expires:
                        cache_file.unlink()
                        return None
                    return data.get("value")
                
                return data
            except (json.JSONDecodeError, KeyError):
                return None
        
        return None
    
    def set(self, key: str, value: Any, expiry_hours: Optional[int] = None) -> None:
        """Set a value in cache"""
        cache_file = self.cache_dir / f"{key}.json"
        
        hours = expiry_hours or self.default_expiry_hours
        expires = datetime.now() + timedelta(hours=hours)
        
        data = {
            "value": value,
            "_expires": expires.isoformat(),
            "_created": datetime.now().isoformat()
        }
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, default=str)
    
    def delete(self, key: str) -> bool:
        """Delete a value from cache"""
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()
            return True
        return False
    
    def clear(self) -> int:
        """Clear all cache"""
        return clear_cache(self.cache_dir)
    
    def info(self) -> dict:
        """Get cache information"""
        return get_cache_info(cache_dir=self.cache_dir)


# Example usage
if __name__ == "__main__":
    # Demo the cache decorator
    @file_cache(expiry_hours=1)
    def expensive_computation(x: int, y: int) -> int:
        print(f"Computing {x} + {y}...")
        return x + y
    
    # First call - computes
    result1 = expensive_computation(5, 3)
    print(f"Result 1: {result1}")
    
    # Second call - from cache
    result2 = expensive_computation(5, 3)
    print(f"Result 2: {result2}")
    
    # Show cache info
    print(f"\nCache info: {expensive_computation.cache_info()}")
    
    # Clear cache
    expensive_computation.clear_cache()
    print("Cache cleared")
