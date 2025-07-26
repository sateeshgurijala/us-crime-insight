import pandas as pd
import re

def basic_eda(df: pd.DataFrame):
    print("=== Shape of dataset ===")
    print(df.shape)

    # Fix column names (e.g., remove BOM character)
    df.columns = [col.encode('ascii', 'ignore').decode('utf-8').strip() for col in df.columns]

    print("\n=== Column Names ===")
    print(list(df.columns))

    # Convert Date/Time to datetime
    if 'Date/Time' in df.columns:
        df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== Null Values Per Column ===")
    print(df.isnull().sum())

    # Unique values and counts for selected columns
    for col in ['Agency', 'Crime', 'Public_Address']:
        print(f"\n=== Unique value counts for '{col}' ===")
        print(df[col].value_counts())

    # Print date range
    if 'Date/Time' in df.columns:
        print("\n=== Date Range ===")
        print("Start:", df['Date/Time'].min())
        print("End  :", df['Date/Time'].max())

    # Create a new column: Cleaned Street Name (remove number prefix like 32XX or 2700 etc.)
    print("\n=== Extracting Street Names from Public_Address ===")

    def extract_street(address):
        if isinstance(address, str):
            return re.sub(r"^[0-9]+[A-Z]*\s+", "", address).strip()
        return None

    df['Street_Name'] = df['Public_Address'].apply(extract_street)

    print("\n=== Unique Cleaned Street Names (Top 20) ===")
    print(df['Street_Name'].value_counts())

