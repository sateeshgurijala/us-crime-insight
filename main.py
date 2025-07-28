# main.py

from data_fetchers.denton_fetcher import fetch_full_crime_data
from data_processing.preprocess_denton import basic_eda
from data.geocoding.geocode_denton import run_geocoding
from data_processing.merge_geocoding import merge_with_geocoding
from dotenv import load_dotenv
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

    # Step 3: Run geocoding on addresses in the dataset
    geocode_df = run_geocoding(df, address_col=address_col, api_key=GOOGLE_API_KEY)

    # Step 4: Merge geocoding results with dataset and save output
    merged_df_geocode = merge_with_geocoding(
        df,
        geocode_df,
        address_col=address_col,
        output_name="denton_processed_with_geocodes.csv"
    )
