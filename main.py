from data_fetchers.denton_fetcher import fetch_full_crime_data
from address_utils.address_validator import validate_addresses_google
from data_processing.preprocess_denton import basic_eda
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Missing Google Maps API key in environment variables.")

if __name__ == "__main__":
    df = fetch_full_crime_data(save_local=False)
    # basic_eda(df)

    validated_df = validate_addresses_google(
        df,
        address_column="Public_Address",
        api_key=GOOGLE_API_KEY,
        limit=50
    )

    print(validated_df[validated_df['status'] != 'VALID'][['address', 'status']])