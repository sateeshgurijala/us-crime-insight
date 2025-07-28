# config/settings.py

from pathlib import Path

# Base directory (root of your project)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Logs
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "preprocess_log.xlsx"

# Cache
CACHE_DIR = DATA_DIR / "cache"
GEOCODE_CACHE_FILE = CACHE_DIR / "geocode_cache.csv"
GEOCODE_CURRENT_RUN_FILE = CACHE_DIR / "geocode_current_run.csv"
