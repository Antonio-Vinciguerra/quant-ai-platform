# main.py

import os
from dotenv import load_dotenv

load_dotenv()

from scripts.clean_eurusd import clean_data
from scripts.resample_eurusd import resample_all
from scripts.seasonality_analysis import analyze_seasonality
from scripts.visualize_seasonality import generate_seasonality_charts
from notion_writer import write_paragraph_to_notion


def main():
    print("🚀 Starting Quant AI pipeline...\n")

    # Step 1: Ingest live data from OANDA
    print("🔌 Ingesting live EUR/USD data from OANDA...")
    os.system("python3 scripts/oanda_ingest.py")  # updated script name

    # Step 2: Clean data
    print("🧹 Cleaning data...")
    clean_data("EURUSD")

    # Step 3: Resample data
    print("🕰️ Resampling all timeframes...")
    resample_all("EURUSD")

    # Step 4: Run seasonal analysis
    print("📈 Running seasonality analysis...")
    analyze_seasonality()

    # Step 5: Generate charts
    print("📊 Visualizing seasonal patterns...")
    generate_seasonality_charts()

    # Step 6: Write update to Notion
    print("🧠 Syncing update to Notion...")
    write_paragraph_to_notion(
        os.getenv("NOTION_PAGE_ID_MASTER"),
        "✅ EUR/USD pipeline run completed with latest OANDA data.")

    print("\n✅ All tasks completed successfully.")


if __name__ == "__main__":
    main()
