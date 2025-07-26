import pandas as pd
import requests
from io import StringIO

# Full CSV export link from Denton city data portal
DENTON_CSV_URL = "https://data.cityofdenton.com/dataset/de9e0c7f-4704-47dc-9501-517808448b64/resource/34f60f26-b458-48d0-9e40-d4f83fee3563/download/dentoncrimedata.csv"


def fetch_full_crime_data(save_local=False):
    """
    Downloads the full Denton crime dataset from the official CSV link.

    Args:
        save_local (bool): If True, saves the file locally as 'denton_crime_data.csv'

    Returns:
        pd.DataFrame: Parsed crime data
    """
    print("Downloading full Denton crime dataset...")
    response = requests.get(DENTON_CSV_URL)

    if response.status_code == 200:
        # Parse CSV content into a DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)

        # Optional: Save to local CSV
        if save_local:
            df.to_csv("denton_crime_data.csv", index=False)
            print("Saved to denton_crime_data.csv")

        print(f"Fetched {len(df)} rows.")
        return df
    else:
        raise Exception(f"Failed to download data: {response.status_code}")
