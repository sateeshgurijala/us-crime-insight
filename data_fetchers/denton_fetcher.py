# data_fetchers/denton_fetcher.py

import pandas as pd
import requests
from io import StringIO
# import requests_cache
# import logging
from config.settings import RAW_DATA_DIR
import os

DENTON_CSV_URL = "https://data.cityofdenton.com/dataset/de9e0c7f-4704-47dc-9501-517808448b64/resource/34f60f26-b458-48d0-9e40-d4f83fee3563/download/dentoncrimedata.csv"

# Enable request caching
# requests_cache.install_cache("denton_fetch_cache", expire_after=3600) # 1-hour cache

# Setup logging
# logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def fetch_full_crime_data(save_local=False) -> pd.DataFrame:
    """
    Downloads the full Denton crime dataset from the official CSV link.

    Args:
        save_local (bool): If True, save the file locally to data/raw/denton_raw.csv

    Returns:
        pd.DataFrame: Parsed crime data
    """
    print("Downloading full Denton crime dataset from website...")
    response = requests.get(DENTON_CSV_URL)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, encoding="utf-8-sig")

        if save_local:
            os.makedirs(RAW_DATA_DIR, exist_ok=True)
            file_path = RAW_DATA_DIR / "denton_raw.csv"
            df.to_csv(file_path, index=False)
            print(f"Saved raw dataset to: {file_path}")

        print(f"Fetched {len(df)} rows.")
        return df
    else:
        raise Exception(f"Failed to download data: HTTP {response.status_code}")
