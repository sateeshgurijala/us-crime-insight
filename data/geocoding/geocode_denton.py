# geocoding/geocode_denton.py

import pandas as pd
from address_utils.address_validator import validate_addresses_google
from address_utils.geocode_cache_handler import load_geocode_cache, save_geocode_cache, get_uncached_addresses
from config.settings import GEOCODE_CURRENT_RUN_FILE
import os

def run_geocoding(df: pd.DataFrame, address_col: str, api_key: str, delay: float = 0.1) -> pd.DataFrame:
    """
    Handles geocoding workflow:
    - Loads existing cache
    - Finds uncached addresses
    - Geocodes new addresses
    - Updates and saves cache
    """
    cache_df = load_geocode_cache()
    cached_addresses = set(cache_df["address"].dropna().unique())
    uncached_df = get_uncached_addresses(df, address_col, cache_df)
    uncached_addresses = uncached_df[address_col].dropna().unique()

    print(f"Total rows in dataset: {len(df)}")
    print(f"Unique addresses in dataset: {len(df[address_col].dropna().unique())}")
    print(f"Already cached: {len(cached_addresses)}")
    print(f"Will geocode {len(uncached_addresses)} new addresses")

    if os.path.exists(GEOCODE_CURRENT_RUN_FILE):
        os.remove(GEOCODE_CURRENT_RUN_FILE)

    if len(uncached_addresses) > 0:
        to_geocode_df = pd.DataFrame(uncached_addresses, columns=["address"])

        new_geocoded_df = validate_addresses_google(
            to_geocode_df,
            address_column="address",
            api_key=api_key,
            delay=delay,
            output_file=GEOCODE_CURRENT_RUN_FILE
        )

        updated_cache = pd.concat([cache_df, new_geocoded_df], ignore_index=True)
        save_geocode_cache(updated_cache)
        print("Geocoding complete. Updated cache saved.")
        return updated_cache

    else:
        print("All addresses already cached. Nothing to geocode.")
        return cache_df
