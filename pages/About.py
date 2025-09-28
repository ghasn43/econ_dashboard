import streamlit as st

st.set_page_config(page_title="About", layout="wide")
st.title("ℹ️ About This Dashboard")

st.markdown("""
### Data Sources
- World Bank Open Data API
- IMF, UNESCO, WHO (future expansion)

### Methodology
- Indicators are fetched directly via API
- Data is cleaned and cached locally
- Forecasts use ARIMA time-series modeling

### Credits
Developed with ❤️ using Python, Streamlit, and Plotly
""")
