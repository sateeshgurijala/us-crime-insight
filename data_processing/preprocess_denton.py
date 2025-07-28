# data_processing/preprocess_denton.py

import pandas as pd
import re

from logs.preprocess_logger import append_preprocess_log

def basic_eda(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic EDA and feature extraction for Denton crime dataset.
    This version does NOT drop rows, but prepares cleaned data and summary insights.

    Returns:
        pd.DataFrame: Modified DataFrame with parsed columns and new features
    """

    # 1. Fix column names — remove BOM characters
    df.columns = [col.encode("ascii", "ignore").decode("utf-8").strip() for col in df.columns]
    # Example: ï»¿ID → ID

    # 2. Print shape
    print("=== Shape of dataset ===")
    print(df.shape)

    # 3. Column names
    print("\n=== Column Names ===")
    print(list(df.columns))

    # 4. Convert Date/Time to datetime (but DO NOT drop bad values)
    if 'Date/Time' in df.columns:
        df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')  # If invalid, becomes NaT — do NOT drop

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== Null Values Per Column ===")
    print(df.isnull().sum())

    # 5. Unique value count summaries — only for these important fields
    for col in ['Agency', 'Crime', 'Public_Address']:
        if col in df.columns:
            print(f"\n=== Unique value counts for '{col}' ===")
            print(df[col].value_counts())
            # Optional: Could log full value_counts to file later

    # 6. Date range summary
    if 'Date/Time' in df.columns:
        print("\n=== Date Range ===")
        print("Start:", df['Date/Time'].min())
        print("End  :", df['Date/Time'].max())

    # 7. Extract cleaned street name from redacted addresses (like "32XX N LOCUST ST" → "N LOCUST ST")
    def extract_street(address):
        if isinstance(address, str):
            return re.sub(r"^[0-9]+[A-Z]*\s+", "", address).strip()
        return None

    if 'Public_Address' in df.columns:
        df['Street_Address'] = df['Public_Address'].apply(extract_street)

        # Commented — optional future insight
        # print("\n=== Unique Cleaned Street Names (Top 20) ===")
        # print(df['Street_Address'].value_counts().head(20))

    # No data drops or filters — all rows remain intact
    # Later we can log unexpected formats to a separate file for QA
    append_preprocess_log(df, dataset_name="denton_raw.csv")

    return df
