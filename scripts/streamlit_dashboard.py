import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime

ENRICHED_DIR = "../knowledge_base/cleaned_enriched"

def load_data():
    records = []

    for file in os.listdir(ENRICHED_DIR):
        if not file.endswith(".json"):
            continue

        filepath = os.path.join(ENRICHED_DIR, file)

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            source = data.get("source", "unknown")
            timestamp = data.get("timestamp", "")

            for item in data.get("items", []):
                records.append({
                    "source": source,
                    "title": item.get("title", ""),
                    "summary": item.get("summary", ""),
                    "sentiment": item.get("sentiment", 0),
                    "timestamp": timestamp
                })
        except Exception as e:
            st.warning(f"Failed to read: {file} | {e}")

    return pd.DataFrame(records)

# Load and process
df = load_data()
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.sort_values(by="timestamp", ascending=False)

st.title("🧠 QuantCopilot Sentiment Dashboard")

# Filter by source
sources = df["source"].unique().tolist()
selected_sources = st.multiselect("🗂 Select Sources", sources, default=sources)

filtered_df = df[df["source"].isin(selected_sources)]

# Sentiment chart
st.subheader("📉 Average Sentiment Over Time")
sentiment_chart = (
    filtered_df
    .groupby([pd.Grouper(key="timestamp", freq="H"), "source"])["sentiment"]
    .mean()
    .unstack()
)
st.line_chart(sentiment_chart)

# Table of recent articles
st.subheader("📰 Recent Headlines")
st.dataframe(filtered_df[["timestamp", "source", "title", "sentiment"]].head(25))
