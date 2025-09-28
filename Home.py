

import streamlit as st
import plotly.express as px
import pandas as pd
from utils import get_wb_data, INDICATORS, COUNTRIES
# 🔹 Experts Group Branding
st.markdown(
    """
    <div style="text-align:center; padding:15px; margin-bottom:20px; border-bottom:2px solid #002b5c;">
        <h1 style="margin:0; font-size:40px; color:#002b5c; font-family:Helvetica, Arial, sans-serif;">
            Experts Group
        </h1>
        <p style="margin:0; font-size:18px; color:#555; font-style:italic;">
            Innovating Economics & Education Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <head>
      <meta property="og:title" content="📊 Economic Dashboard" />
      <meta property="og:description" content="Interactive dashboard to explore GDP, Inflation, Employment, and Education data worldwide." />
      <meta property="og:image" content="https://yourdomain.com/preview.png" />
      <meta property="og:url" content="https://yourusername-economic-dashboard.streamlit.app" />
      <meta name="twitter:card" content="summary_large_image" />
    </head>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Economic Dashboard", layout="wide")
st.title("📊 Economic Indicators Dashboard")

# User input
selected_countries = st.multiselect(
    "🌍 Select Countries:",
    list(COUNTRIES.keys()),
    default=["United Arab Emirates", "United States"]
)

year_range = st.slider(
    "📅 Select Year Range:",
    min_value=1960, max_value=2023, value=(2000, 2023)
)
start_year, end_year = year_range

# Preview charts
st.markdown("### 📌 Explore Indicators")

for ind_name, ind_code in INDICATORS.items():
    df = pd.DataFrame()
    for country in selected_countries:
        data = get_wb_data(COUNTRIES[country], ind_code, start_year, end_year)
        if not data.empty:
            data = data.rename(columns={"value": country})
            df = pd.concat([df, data], axis=1)
    if not df.empty:
        df_long = df.reset_index().melt(id_vars="date", var_name="Country", value_name="Value")
        fig = px.line(df_long, x="date", y="Value", color="Country", title=f"{ind_name} (Preview)")
        fig.update_layout(template="plotly_white", height=300, font=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)
        st.page_link(f"pages/{ind_name.split()[0]}.py", label=f"🔍 View Full {ind_name}")
