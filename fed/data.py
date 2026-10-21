import pandas as pd
import requests

def load_gdp_data():
    """Download annual GDP data for seven countries, 2000–2022."""

    countries = "GBR;USA;BRA;JPN;CHN;DEU;CHE"

    url = (
        f"https://api.worldbank.org/v2/country/{countries}/"
        "indicator/NY.GDP.MKTP.CD"
    )

    params = {
        "format": "json",
        "date": "2000:2022",
        "per_page": 1000
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if len(data) < 2 or data[1] is None:
        raise ValueError("No GDP observations returned.")

    df = pd.DataFrame(data[1])

    return df

def clean_gdp_data(raw_df):
    """Clean World Bank GDP data for analysis."""

    # 1. Select the columns we need from original raw dataset
    df = raw_df[["countryiso3code", "date", "value"]].copy()

    # 2. Rename columns
    df = df.rename(columns={
        "countryiso3code": "country",
        "date": "year",
        "value": "gdp_usd"
    })

    # 3. Convert columns to numeric types
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["gdp_usd"] = pd.to_numeric(df["gdp_usd"], errors="coerce")

    # 4. Remove rows with missing essential values
    df = df.dropna(subset=["country", "year", "gdp_usd"])

    # 5. Convert year to an integer
    df["year"] = df["year"].astype(int)

    # 6. Keep observations between 2000 and 2022
    df = df[(df["year"] >= 2000) & (df["year"] <= 2022)].copy()

    # 7. Convert GDP to trillions of US dollars
    df["gdp_usd_trillions"] = df["gdp_usd"] / 1_000_000_000_000

    # 8. Sort by country and year
    df = df.sort_values(["country", "year"])

    # 9. Reset the row index
    df = df.reset_index(drop=True)

    return df