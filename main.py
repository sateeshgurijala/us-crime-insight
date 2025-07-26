from data_fetchers.denton_fetcher import fetch_full_crime_data
from data_processing.preprocess_denton import basic_eda

if __name__ == "__main__":
    df = fetch_full_crime_data(save_local=False)
    basic_eda(df)
