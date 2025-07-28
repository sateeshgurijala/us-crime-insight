import pandas as pd
import os
from config.settings import GEOCODE_CACHE_FILE


def load_geocode_cache():
    if os.path.exists(GEOCODE_CACHE_FILE):
        return pd.read_csv(GEOCODE_CACHE_FILE)
    else:
        return pd.DataFrame(columns=["address", "latitude", "longitude", "status"])

def save_geocode_cache(df: pd.DataFrame):
    os.makedirs(GEOCODE_CACHE_FILE.parent, exist_ok=True)
    df.to_csv(GEOCODE_CACHE_FILE, index=False)

def get_uncached_addresses(df: pd.DataFrame, address_column: str, cache_df: pd.DataFrame):
    cached_addresses = set(cache_df["address"].dropna().unique())
    return df[~df[address_column].isin(cached_addresses)]
