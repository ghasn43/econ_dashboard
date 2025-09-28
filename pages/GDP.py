import streamlit as st
import plotly.express as px
import pandas as pd
from utils import get_wb_data, INDICATORS, COUNTRIES

st.set_page_config(page_title="GDP (current US$)", layout="wide")
st.title("🌍 GDP (current US$)")

countries = st.multiselect("Select Countries:", list(COUNTRIES.keys()), ["United Arab Emirates", "United States"])
years = st.slider("Year Range:", 1960, 2023, (2000, 2023))
start, end = years

df = pd.DataFrame()
for c in countries:
    data = get_wb_data(COUNTRIES[c], INDICATORS["GDP (current US$)"], start, end)
    if not data.empty:
        data = data.rename(columns={"value": c})
        if df.empty:
            df = data
        else:
            df = df.join(data, how="outer", rsuffix=f"_{c}")

if not df.empty:
    df = df.reset_index().rename(columns={"date": "Year"})
    fig = px.line(df, x="Year", y=df.columns[1:], title="GDP (current US$)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)
