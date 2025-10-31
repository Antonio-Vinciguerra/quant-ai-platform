import streamlit as st
import pandas as pd
import plotly.express as px
from deep_translator import GoogleTranslator
from datetime import datetime, timezone
import os

### --------------------- UI CONFIG -----------------------
st.set_page_config(page_title="QuantCopilot Sentiment Dashboard", layout="wide")

st.title("🧠 QuantCopilot — Sentiment Intelligence Dashboard")

st.caption(
    "Live sentiment from financial news sources — filter, explore & translate headlines."
)

### --------------------- LOAD DATA -----------------------
DATA_PATH = "../processed/sentiment_enriched.parquet"

if not os.path.exists(DATA_PATH):
    st.error(f"Data file not found: {DATA_PATH}")
    st.stop()

df = pd.read_parquet(DATA_PATH)

### --------------------- NORMALIZE STRUCTURE -----------------------
def expand_row(row):
    records = []
    for item in row.get("items", []):
        records.append({
            "source": row.get("source"),
            "timestamp": row.get("timestamp"),
            "title": item.get("title",""),
            "link": item.get("link",""),
            "summary": item.get("summary","")
        })
    return pd.DataFrame(records)

expanded = []
for _, r in df.iterrows():
    expanded.append(expand_row(r))

df = pd.concat(expanded, ignore_index=True)

### --------------------- CLEAN DATES -----------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date

### --------------------- SIDEBAR FILTERS -----------------------
st.sidebar.header("🔍 Filters")

# Language
translate = st.sidebar.checkbox("🌍 Translate to English", value=False)

# Date range
date_min, date_max = df["date"].min(), df["date"].max()
selected_dates = st.sidebar.date_input("Select Date Range", [date_min, date_max])

# Sentiment Score slider fallback (some runs may not have this yet)
min_score = df.get("sentiment_score", pd.Series([0])).min()
max_score = df.get("sentiment_score", pd.Series([1])).max()

score_range = st.sidebar.slider(
    "Sentiment Score Range",
    float(min_score),
    float(max_score),
    (float(min_score), float(max_score))
)

# Sources
sources = sorted(df["source"].dropna().unique())
selected_sources = st.sidebar.multiselect("Sources", sources, default=sources)

### --------------------- APPLY FILTERS -----------------------
filtered = df.copy()
filtered = filtered[
    (filtered["date"] >= selected_dates[0]) & 
    (filtered["date"] <= selected_dates[-1]) &
    (filtered["source"].isin(selected_sources))
]

if "sentiment_score" in filtered.columns:
    filtered = filtered[
        (filtered["sentiment_score"] >= score_range[0]) &
        (filtered["sentiment_score"] <= score_range[1])
    ]

### --------------------- TRANSLATION -----------------------
if translate:
    with st.spinner("Translating headlines..."):
        filtered["title"] = filtered["title"].apply(
            lambda x: GoogleTranslator(source='auto', target='en').translate(x) if x else x
        )

### --------------------- SENTIMENT CHART -----------------------
if "sentiment_score" in filtered.columns:
    st.subheader("📈 Sentiment Over Time")

    chart = px.line(
        filtered.sort_values("timestamp"),
        x="timestamp",
        y="sentiment_score",
        color="source",
        title="Sentiment Score Trend",
    )
    st.plotly_chart(chart, use_container_width=True)
else:
    st.warning("No sentiment scores available in this dataset yet.")

### --------------------- NEWS TABLE -----------------------
st.subheader("📰 Latest Headlines")

st.dataframe(
    filtered[["timestamp", "source", "title"]].sort_values("timestamp", ascending=False),
    use_container_width=True
)

### --------------------- FOOTER -----------------------
st.caption(
    f"Last run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  |  Built by Antonio 🚀"
)
