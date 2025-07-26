import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded
import time


def validate_addresses_google(
        df: pd.DataFrame,
        address_column: str = "address",
        api_key: str = "",
        delay: float = 0.2,
        limit: int = None
) -> pd.DataFrame:
    """
    Geocode addresses using Google Maps API and return a new DataFrame with results.

    Args:
        df (pd.DataFrame): The input DataFrame.
        address_column (str): Column name containing the address.
        api_key (str): Google Maps API key.
        delay (float): Delay between API calls (to avoid quota issues).
        limit (int): Max number of rows to validate (for testing). None = full dataset.

    Returns:
        pd.DataFrame: A new DataFrame with original address, lat, lon, and status.
    """
    if not api_key:
        raise ValueError("You must provide a valid Google Maps API key.")

    geolocator = GoogleV3(api_key=api_key, timeout=10)
    results = []

    subset = df if limit is None else df.head(limit)

    for i, row in subset.iterrows():
        address = row[address_column]
        try:
            location = geolocator.geocode(address)
            if location:
                results.append({
                    "original_index": i,
                    "address": address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "status": "VALID"
                })
            else:
                results.append({
                    "original_index": i,
                    "address": address,
                    "latitude": None,
                    "longitude": None,
                    "status": "NOT_FOUND"
                })
        except (GeocoderTimedOut, GeocoderQuotaExceeded):
            results.append({
                "original_index": i,
                "address": address,
                "latitude": None,
                "longitude": None,
                "status": "ERROR"
            })
        time.sleep(delay)  # be polite to the API

    return pd.DataFrame(results)
