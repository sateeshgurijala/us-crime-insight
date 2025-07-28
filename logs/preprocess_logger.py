# logs/preprocess_logger.py

import pandas as pd
import os
from datetime import datetime
from config.settings import LOG_FILE




def append_preprocess_log(
    df: pd.DataFrame,
    dataset_name: str,
    notes: str = "",
):
    """
    Appends a new log entry to the shared preprocessing Excel log.

    Args:
        df (pd.DataFrame): The DataFrame being analyzed
        dataset_name (str): Identifier (e.g., denton_raw.csv)
        notes (str): Optional notes or warnings
    """
    # Generate EDA metrics
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    shape = f"{df.shape[0]} rows, {df.shape[1]} cols"
    columns = ", ".join(df.columns)
    dtypes = ", ".join(f"{col}:{dtype}" for col, dtype in df.dtypes.items())
    null_counts = ", ".join(f"{col}:{df[col].isnull().sum()}" for col in df.columns)

    if "Date/Time" in df.columns and pd.api.types.is_datetime64_any_dtype(df["Date/Time"]):
        date_range = f"{df['Date/Time'].min()} to {df['Date/Time'].max()}"
    else:
        date_range = "N/A"

    log_entry = {
        "Timestamp": timestamp,
        "Dataset": dataset_name,
        "Shape": shape,
        "Columns": columns,
        "Data Types": dtypes,
        "Null Counts": null_counts,
        "Date Range": date_range,
        "Notes": notes,
    }

    # Load existing logs if present
    if os.path.exists(LOG_FILE):
        existing_log = pd.read_excel(LOG_FILE)
        updated_log = pd.concat([existing_log, pd.DataFrame([log_entry])], ignore_index=True)
    else:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        updated_log = pd.DataFrame([log_entry])

    # Save updated log
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    updated_log.to_excel(LOG_FILE, index=False)
    print(f"Preprocess log appended to {LOG_FILE}")
