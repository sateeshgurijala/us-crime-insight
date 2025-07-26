import pandas as pd

def basic_eda(df: pd.DataFrame):
    print("=== Shape of dataset ===")
    print(df.shape)

    print("\n=== Column Names ===")
    print(df.columns.tolist())

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== Null Values Per Column ===")
    print(df.isnull().sum())

    print("\n=== Unique value counts (first few columns) ===")
    for col in df.columns[:5]:
        print(f"\nUnique values in '{col}':")
        print(df[col].value_counts(dropna=False).head(10))
