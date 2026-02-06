"""
Logging utilities for Greene County Property Finder

Usage:
    from utils.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Starting application")
    logger.error("Something went wrong", exc_info=True)
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import os


# Log format constants
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DETAILED_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
SIMPLE_FORMAT = "%(levelname)s: %(message)s"

# Color codes for terminal output
COLORS = {
    'DEBUG': '\033[36m',     # Cyan
    'INFO': '\033[32m',      # Green
    'WARNING': '\033[33m',   # Yellow
    'ERROR': '\033[31m',     # Red
    'CRITICAL': '\033[35m',  # Magenta
    'RESET': '\033[0m'       # Reset
}


class ColoredFormatter(logging.Formatter):
    """Formatter that adds colors to log output for terminals"""
    
    def __init__(self, fmt: str = DEFAULT_FORMAT, use_colors: bool = True):
        super().__init__(fmt)
        self.use_colors = use_colors and sys.stdout.isatty()
    
    def format(self, record: logging.LogRecord) -> str:
        if self.use_colors:
            color = COLORS.get(record.levelname, COLORS['RESET'])
            reset = COLORS['RESET']
            record.levelname = f"{color}{record.levelname}{reset}"
        return super().format(record)


def setup_logger(
    name: str = "property_finder",
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    use_colors: bool = True
) -> logging.Logger:
    """
    Set up and configure a logger
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs
        log_to_console: Whether to output to console
        use_colors: Whether to use colored output in console
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Set level from string
    level_num = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level_num)
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level_num)
        console_handler.setFormatter(ColoredFormatter(DEFAULT_FORMAT, use_colors))
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level_num)
        file_handler.setFormatter(logging.Formatter(DETAILED_FORMAT))
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = "property_finder") -> logging.Logger:
    """
    Get or create a logger with the given name
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set up defaults
    if not logger.handlers:
        level = os.environ.get("LOG_LEVEL", "INFO")
        log_file = os.environ.get("LOG_FILE_PATH")
        setup_logger(name, level, log_file)
    
    return logger


class LogContext:
    """Context manager for logging operations with timing"""
    
    def __init__(self, logger: logging.Logger, operation: str, level: int = logging.INFO):
        self.logger = logger
        self.operation = operation
        self.level = level
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.log(self.level, f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.log(self.level, f"Completed: {self.operation} ({duration:.2f}s)")
        else:
            self.logger.error(f"Failed: {self.operation} ({duration:.2f}s) - {exc_val}")
        
        return False  # Don't suppress exceptions


# Convenience function for timed operations
def log_operation(logger: logging.Logger, operation: str):
    """
    Decorator/context manager for logging operations with timing
    
    Usage:
        with log_operation(logger, "Fetching data"):
            fetch_data()
    """
    return LogContext(logger, operation)


# Example usage
if __name__ == "__main__":
    # Demo the logger
    logger = setup_logger("demo", level="DEBUG", use_colors=True)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    with log_operation(logger, "Demo operation"):
        import time
        time.sleep(0.5)
        print("Doing work...")
