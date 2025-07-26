import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded
import time
import os

def validate_addresses_google(
    df: pd.DataFrame,
    address_column: str = "address",
    api_key: str = "",
    delay: float = 0.2,
    limit: int = None,
    output_file: str = "data/geocode_current_run.csv"
) -> pd.DataFrame:
    """
    Geocode addresses using Google Maps API and return a DataFrame of new results.
    Saves progress row-by-row to avoid losing work.
    """
    if not api_key:
        raise ValueError("You must provide a valid Google Maps API key.")

    geolocator = GoogleV3(api_key=api_key, timeout=10)
    results = []

    subset = df if limit is None else df.head(limit)
    total = len(subset)

    # Ensure 'data/' folder exists
    os.makedirs("data", exist_ok=True)

    for i, row in subset.iterrows():
        address = row[address_column]
        print(f"[{len(results) + 1}/{total}] Geocoding: {address}")

        try:
            location = geolocator.geocode(address)
            if location:
                result = {
                    "original_index": i,
                    "address": address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "status": "VALID"
                }
            else:
                result = {
                    "original_index": i,
                    "address": address,
                    "latitude": None,
                    "longitude": None,
                    "status": "NOT_FOUND"
                }
        except (GeocoderTimedOut, GeocoderQuotaExceeded):
            result = {
                "original_index": i,
                "address": address,
                "latitude": None,
                "longitude": None,
                "status": "ERROR"
            }

        results.append(result)

        # ✅ Real-time cache saving: keep overwriting the current batch
        pd.DataFrame(results).to_csv(output_file, index=False)

        time.sleep(delay)

    return pd.DataFrame(results)
