import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="QuantCopilot Dashboard", layout="wide")
st.title("🧠 QuantCopilot Dashboard")

# === Config ===
data_root = "../processed"
symbols = sorted([d for d in os.listdir(data_root) if os.path.isdir(os.path.join(data_root, d))])
timeframes = ["M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]

# === Sidebar: Symbol + Timeframe selector ===
st.sidebar.header("⚙️ Data Selection")
selected_symbol = st.sidebar.selectbox("Select symbol", symbols)
selected_tf = st.sidebar.selectbox("Select timeframe", timeframes)

# === File path ===
file_path = os.path.join(data_root, selected_symbol, f"{selected_symbol}_{selected_tf}.parquet")

# === Load Data ===
if os.path.exists(file_path):
    df = pd.read_parquet(file_path)
    st.success(f"✅ Loaded {selected_symbol} at {selected_tf}")

    # === Preview ===
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # === Summary Stats ===
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # === Plot Range_Pips if available ===
    if "Range_Pips" in df.columns:
        st.subheader("📉 Range_Pips Distribution")
        fig, ax = plt.subplots()
        df["Range_Pips"].plot.hist(bins=50, ax=ax)
        st.pyplot(fig)
    else:
        st.info("ℹ️ No 'Range_Pips' column found.")
else:
    st.error(f"❌ File not found: {file_path}")
