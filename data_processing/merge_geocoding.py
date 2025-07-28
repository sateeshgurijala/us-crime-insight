# data_processing/merge_geocoding.py

import pandas as pd
import os
from config.settings import PROCESSED_DATA_DIR

def merge_with_geocoding(
    df: pd.DataFrame,
    geocode_df: pd.DataFrame,
    address_col: str,
    output_name: str = "denton_processed_with_geocodes.csv"
) -> pd.DataFrame:
    """
    Merges processed data with geocode results and saves to a separate CSV file.

    Args:
        df (pd.DataFrame): The preprocessed dataset
        geocode_df (pd.DataFrame): Geocoding results (cache or fresh)
        address_col (str): Column to match (e.g., Public_Address)
        output_name (str): Name for the output file (relative to processed folder)

    Returns:
        pd.DataFrame: Merged dataset
    """
    # Align address column if needed
    geocode_df = geocode_df.rename(columns={"address": address_col})

    merged_df = df.merge(geocode_df, on=address_col, how="left")

    # Save separately
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / output_name
    merged_df.to_csv(output_path, index=False)
    print(f"Merged geocode data saved to: {output_path}")

    return merged_df
