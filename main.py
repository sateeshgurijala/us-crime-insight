# main.py

from data_fetchers.denton_fetcher import fetch_full_crime_data
from address_utils.address_validator import validate_addresses_google
from address_utils.geocode_cache_handler import load_geocode_cache, save_geocode_cache, get_uncached_addresses
from data_processing.preprocess_denton import basic_eda
from config.settings import GEOCODE_CURRENT_RUN_FILE
from dotenv import load_dotenv
import pandas as pd
import os

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
address_col = "Public_Address"

if not GOOGLE_API_KEY:
    raise ValueError("Missing Google Maps API key in environment variables.")

if __name__ == "__main__":
    # Step 1: Fetch latest raw data and save to /data/raw
    df = fetch_full_crime_data(save_local=True)

    # Step 2: Preprocess and log characteristics (EDA)
    df = basic_eda(df)

    # Step 3: Load existing geocode cache
    cache_df = load_geocode_cache()
    cached_addresses = set(cache_df["address"].dropna().unique())

    # Step 4: Extract unique new addresses from dataset
    all_addresses = df[address_col].dropna().unique()
    uncached_df = get_uncached_addresses(df, address_col, cache_df)
    uncached_addresses = uncached_df[address_col].dropna().unique()

    print(f"Total rows in dataset: {len(df)}")
    print(f"Unique addresses in dataset: {len(all_addresses)}")
    print(f"Already cached: {len(cached_addresses)}")
    print(f"Will geocode {len(uncached_addresses)} new addresses")

    # Step 5: Clear current run file if exists
    if os.path.exists(GEOCODE_CURRENT_RUN_FILE):
        os.remove(GEOCODE_CURRENT_RUN_FILE)

    # Step 6: Run geocoding on uncached addresses only
    if uncached_addresses:
        to_geocode_df = pd.DataFrame(uncached_addresses, columns=["address"])

        new_geocoded_df = validate_addresses_google(
            to_geocode_df,
            address_column="address",
            api_key=GOOGLE_API_KEY,
            delay=0.1,
            output_file=GEOCODE_CURRENT_RUN_FILE  # Save progress live
        )

        # Step 7: Update geocode cache with new results
        frames = [df for df in [cache_df, new_geocoded_df] if not df.empty]
        updated_cache = pd.concat(frames, ignore_index=True)
        save_geocode_cache(updated_cache)

        print("Geocoding complete. Updated cache saved.")
    else:
        print("All addresses already cached. Nothing to geocode.")
