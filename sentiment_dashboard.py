import os
import json
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from googletrans import Translator
from streamlit_autorefresh import st_autorefresh

# Load API Keys
load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")

# Auto refresh every 5 mins
st_autorefresh(interval=5 * 60 * 1000, key="refresh")

# --------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="QuantCopilot Sentiment Dashboard", layout="wide")

# Sidebar UI
st.sidebar.title("⚙️ Settings")

# Theme toggle
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("<style>body {background-color:#0E1117; color:white;}</style>", unsafe_allow_html=True)

# Language selection
translate_lang = st.sidebar.selectbox("🌍 Translate to:", ["English", "Spanish", "Portuguese", "Italian", "French"])

translator = Translator()

# ----------- Load Sentiment Data ----------- #
df = pd.read_parquet("../processed/sentiment_enriched.parquet")

# Expand nested article lists safely
def expand_row(row):
    items = row["items"]
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except:
            return pd.DataFrame()
    if isinstance(items, dict):
        items = [items]

    rows = []
    for item in items:
        if isinstance(item, dict):
            rows.append({
                "source": row["source"],
                "timestamp": row["timestamp"],
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "sentiment": row["sentiment"],
                "sentiment_score": row["sentiment_score"]
            })
    return pd.DataFrame(rows)

expanded = []
for _, row in df.iterrows():
    expanded.append(expand_row(row))

df = pd.concat(expanded, ignore_index=True)

# Clean date column
try:
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
except:
    df["date"] = None

# Sidebar filters
st.sidebar.header("🔎 Filters")
sources = st.sidebar.multiselect("News Source", df["source"].unique(), default=df["source"].unique())
sent_min, sent_max = st.sidebar.slider("Sentiment Range", -1.0, 1.0, (-1.0, 1.0))
start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())

# Filter data
mask = (
    df["source"].isin(sources)
    & (df["sentiment_score"] >= sent_min)
    & (df["sentiment_score"] <= sent_max)
    & (df["date"] >= start_date)
    & (df["date"] <= end_date)
)

filtered = df[mask]

# Translate if needed
def maybe_translate(text):
    if translate_lang == "English":
        return text
    try:
        return translator.translate(text, dest=translate_lang.lower()).text
    except:
        return text

filtered["title"] = filtered["title"].apply(maybe_translate)

# ------------ Sentiment Line Chart ------------ #
st.title("📈 Market Sentiment Dashboard")

if not filtered.empty:
    avg_daily = filtered.groupby("date")["sentiment_score"].mean().reset_index()
    fig = px.line(avg_daily, x="date", y="sentiment_score", title="Average Sentiment Over Time")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠ No data for selected filters.")

# ------------ Headlines Preview ------------ #
st.subheader("📰 Latest Headlines")
st.dataframe(filtered[["date", "source", "title", "sentiment_score"]].tail(20), use_container_width=True)

# ------------ Economic Calendar -------------- #
st.subheader("📅 Economic Calendar")

today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

fmp_url = f"https://financialmodelingprep.com/api/v3/economic_calendar?from={today}&to={today}&apikey={FMP_API_KEY}"

try:
    econ = pd.read_json(fmp_url)
    if econ.empty:
        st.info("ℹ️ No major events today or API limit reached")
    else:
        econ = econ[["date", "country", "event", "impact", "actual", "forecast", "previous"]]
        st.dataframe(econ, use_container_width=True)
except Exception as e:
    st.error(f"❌ Failed to fetch economic calendar.\n\nError: {e}")

# Footer
st.markdown("---")
st.markdown("Built with 💙 by Antonio & QuantCopilot GPT")
