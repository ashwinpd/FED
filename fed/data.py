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