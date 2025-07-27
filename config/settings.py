# config/settings.py
import os

# Automatically determine project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data folders
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Geocoding
GEO_CACHE_FILE = os.path.join(DATA_DIR, "geocode_cache.csv")
GEO_CURRENT_RUN_FILE = os.path.join(DATA_DIR, "geocode_current_run.csv")
