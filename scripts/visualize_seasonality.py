import os
import pandas as pd
import matplotlib.pyplot as plt
from scripts.pipeline import get_filtered_data

# ===== SETTINGS =====
SYMBOL = "EURUSD"
OUTPUT_FOLDER = f"../processed/{SYMBOL}"
SUMMARY_FILE = os.path.join(OUTPUT_FOLDER, "seasonality_summary.csv")
# ====================

def load_seasonality_summary():
    if not os.path.exists(SUMMARY_FILE):
        print(f"⚠️ Summary file not found at {SUMMARY_FILE}")
        return None
    df = pd.read_csv(SUMMARY_FILE, index_col=0)
    return df

def plot_range(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Range_Pips_mean"], marker='o')
    plt.title(f"{SYMBOL} – Average Monthly Range (Pips)")
    plt.ylabel("Pips")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_bullish_ratio(df):
    plt.figure(figsize=(10, 5))
    plt.bar(df.index, df["Bullish_Ratio"], color='green')
    plt.axhline(0.5, color='gray', linestyle='--')
    plt.title(f"{SYMBOL} – Bullish Candle Ratio per Month")
    plt.ylabel("% Bullish")
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

def plot_body_size(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Body_Pips_mean"], marker='s', color='orange')
    plt.title(f"{SYMBOL} – Average Monthly Body Size (Pips)")
    plt.ylabel("Pips")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    df = load_seasonality_summary()
    if df is None:
        return
    print(f"📊 Plotting from summary file with columns: {df.columns.tolist()}")
    plot_range(df)
    plot_body_size(df)
    plot_bullish_ratio(df)

if __name__ == "__main__":
    main()


def generate_seasonality_charts():
    print("📊 Generating charts (placeholder)...")
