import pandas as pd
import requests

# Indicators dictionary
INDICATORS = {
    "GDP (current US$)": "NY.GDP.MKTP.CD",
    "Inflation (CPI %)": "FP.CPI.TOTL.ZG",
    "Unemployment (%)": "SL.UEM.TOTL.ZS",
    "Education expenditure (% of GDP)": "SE.XPD.TOTL.GD.ZS"
}

# Countries dictionary
COUNTRIES = {
    "United Arab Emirates": "ARE",
    "United States": "USA",
    "Jordan": "JOR",
    "Saudi Arabia": "SAU",
    "Qatar": "QAT",
    "Egypt": "EGY"
}

def get_wb_data(country_code, indicator_code, start=2000, end=2023):
    """Fetch data from World Bank API for given country and indicator"""
    url = (
        f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
        f"?date={start}:{end}&format=json&per_page=1000"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return pd.DataFrame()

    json_data = response.json()
    if not json_data or len(json_data) < 2:
        return pd.DataFrame()

    df = pd.DataFrame(json_data[1])
    df = df[["date", "value"]].dropna()
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    return df
