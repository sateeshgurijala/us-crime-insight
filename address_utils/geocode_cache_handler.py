import pandas as pd
import os

CACHE_FILE = "data/geocode_cache.csv"

def load_geocode_cache():
    if os.path.exists(CACHE_FILE):
        return pd.read_csv(CACHE_FILE)
    else:
        return pd.DataFrame(columns=["address", "latitude", "longitude", "status"])

def save_geocode_cache(df: pd.DataFrame):
    df.to_csv(CACHE_FILE, index=False)

def get_uncached_addresses(df: pd.DataFrame, address_column: str, cache_df: pd.DataFrame):
    cached_addresses = set(cache_df["address"].dropna().unique())
    return df[~df[address_column].isin(cached_addresses)]
