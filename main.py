from data_fetchers.denton_fetcher import fetch_full_crime_data

if __name__ == "__main__":
    df = fetch_full_crime_data(save_local=False)
    print(df.head())
