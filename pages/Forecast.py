import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from utils import get_wb_data, INDICATORS, COUNTRIES

st.set_page_config(page_title="Forecast", layout="wide")
st.title("🔮 Forecast (Next 5 Years)")

indicator = st.selectbox("Select Indicator:", list(INDICATORS.keys()))
country = st.selectbox("Select Country:", list(COUNTRIES.keys()))
years = st.slider("Year Range:", 1960, 2023, (2000, 2023))
start, end = years

data = get_wb_data(COUNTRIES[country], INDICATORS[indicator], start, end)

if not data.empty and len(data) > 10:
    series = data["value"].dropna()
    model = ARIMA(series, order=(1,1,1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)
    forecast_years = pd.date_range(series.index[-1], periods=6, freq="Y")[1:]
    forecast_df = pd.Series(forecast.values, index=forecast_years)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode="lines", name="Historical"))
    fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df.values, mode="lines+markers", name="Forecast"))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(forecast_df)
else:
    st.warning("Not enough data for forecasting")
