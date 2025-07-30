import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="QuantCopilot Dashboard", layout="wide")
st.title("🧠 QuantCopilot Dashboard")

# === File uploader ===
uploaded_file = st.file_uploader("Upload a cleaned CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=True, index_col=0)
    st.success("✅ File loaded!")

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
    st.info("⬆️ Upload a CSV file to get started.")