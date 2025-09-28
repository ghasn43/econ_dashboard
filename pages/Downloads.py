import streamlit as st
import pandas as pd
from utils import get_wb_data, INDICATORS, COUNTRIES

st.set_page_config(page_title="Downloads", layout="wide")
st.title("⬇️ Download All Data")

countries = st.multiselect("Select Countries:", list(COUNTRIES.keys()), ["United Arab Emirates", "United States"])
years = st.slider("Year Range:", 1960, 2023, (2000, 2023))
start, end = years

all_data = {}
for ind, code in INDICATORS.items():
    df = pd.DataFrame()
    for c in countries:
        data = get_wb_data(COUNTRIES[c], code, start, end)
        if not data.empty:
            data = data.rename(columns={"value": c})
            df = pd.concat([df, data], axis=1)
    if not df.empty:
        all_data[ind] = df

if all_data:
    combined = pd.concat(all_data, axis=1)
    st.dataframe(combined)
    st.download_button(
        "Download CSV",
        combined.to_csv().encode("utf-8"),
        "all_indicators.csv",
        "text/csv"
    )
