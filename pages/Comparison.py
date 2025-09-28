import streamlit as st
import plotly.express as px
import pandas as pd
from utils import get_wb_data, INDICATORS, COUNTRIES

st.set_page_config(page_title="Comparison", layout="wide")
st.title("📊 Compare Indicators")

countries = st.multiselect("Select Countries:", list(COUNTRIES.keys()), ["United Arab Emirates", "United States"])
indicators = st.multiselect("Select Indicators:", list(INDICATORS.keys()), ["GDP (current US$)", "Inflation (CPI %)"])
years = st.slider("Year Range:", 1960, 2023, (2000, 2023))
start, end = years

for ind in indicators:
    df = pd.DataFrame()
    for c in countries:
        data = get_wb_data(COUNTRIES[c], INDICATORS[ind], start, end)
        if not data.empty:
            data = data.reset_index().rename(columns={"date": "Year", "value": c})
            if df.empty:
                df = data[["Year", c]]
            else:
                df = pd.merge(df, data[["Year", c]], on="Year", how="outer")

    if not df.empty:
        df = df.sort_values("Year")
        fig = px.line(df, x="Year", y=df.columns[1:], title=ind)
        fig.update_layout(template="plotly_white", height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)
