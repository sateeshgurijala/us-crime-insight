from data_fetchers.denton_fetcher import fetch_full_crime_data
from address_utils.address_validator import validate_addresses_google
from address_utils.geocode_cache_handler import load_geocode_cache, save_geocode_cache
# from data_processing.preprocess_denton import basic_eda
from dotenv import load_dotenv
import pandas as pd
import os


# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
address_col = "Public_Address"
CACHE_PATH = "data/geocode_cache.csv"
CURRENT_RUN_PATH = "data/geocode_current_run.csv"

if not GOOGLE_API_KEY:
    raise ValueError("Missing Google Maps API key in environment variables.")

if __name__ == "__main__":
    # Step 1: Fetch data
    df = fetch_full_crime_data(save_local=False)

    # Step 2: Load cache (previously geocoded)
    cache_df = load_geocode_cache()
    cached_addresses = set(cache_df["address"].dropna().unique())

    # Step 3: Create list of unique addresses in new dataset
    all_addresses = df[address_col].dropna().unique()
    uncached_addresses = [addr for addr in all_addresses if addr not in cached_addresses]

    print(f"Total rows in dataset: {len(df)}")
    print(f"Unique addresses in dataset: {len(all_addresses)}")
    print(f"Already cached: {len(cached_addresses)}")
    print(f" Will geocode {len(uncached_addresses)} new addresses")

    # Step 4: Clean slate - remove current run file if exists
    if os.path.exists(CURRENT_RUN_PATH):
        os.remove(CURRENT_RUN_PATH)

    # Step 5: Prepare DataFrame of new addresses to geocode
    if uncached_addresses:
        to_geocode_df = pd.DataFrame(uncached_addresses, columns=["address"])

        # Step 6: Run geocoding
        new_geocoded_df = validate_addresses_google(
            to_geocode_df,
            address_column="address",
            api_key=GOOGLE_API_KEY,
            delay=0.1,
            output_file=CURRENT_RUN_PATH  # 👈 Save progress live
        )

        # Step 7: Save full updated cache
        frames = [df for df in [cache_df, new_geocoded_df] if not df.empty]
        updated_cache = pd.concat(frames, ignore_index=True)
        save_geocode_cache(updated_cache)

        print(" Geocoding complete. Updated cache saved.")
    else:
        print(" All addresses already cached. Nothing to geocode.")
