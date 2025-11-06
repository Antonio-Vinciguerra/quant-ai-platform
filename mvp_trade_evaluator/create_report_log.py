import os
import csv
from datetime import datetime

LOG_FILE = "report_log.csv"

def log_report(stats, feedback="", filename="trade_report_output.pdf"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as log:
        writer = csv.writer(log)

        if not log_exists:
            writer.writerow(["Timestamp", "Filename", "Total Profit", "Num Trades", "Win Rate", "Avg Profit", "Max Win", "Max Loss", "Feedback"])

        writer.writerow([
            timestamp,
            filename,
            stats.get("Total Profit", ""),
            stats.get("Number of Trades", ""),
            stats.get("Win Rate", ""),
            stats.get("Average Profit per Trade", ""),
            stats.get("Max Win", ""),
            stats.get("Max Loss", ""),
            feedback.replace("\n", " ")[:300]  # limit feedback length
        ])
