import streamlit as st
import pandas as pd

st.set_page_config(page_title="EUR/USD Dashboard", layout="wide")

st.title("📊 EUR/USD Market Dashboard")

# Load D1 data
df = pd.read_csv("processed/EURUSD/EURUSD_D1.csv")
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Show date range
st.markdown(f"**Date Range:** {df['Datetime'].min().date()} ➝ {df['Datetime'].max().date()}")

# Line chart: Close prices
st.subheader("Daily Closing Prices")
st.line_chart(df.set_index('Datetime')['Close'])

# Show data
if st.checkbox("Show raw data"):
    st.dataframe(df.tail(100))
