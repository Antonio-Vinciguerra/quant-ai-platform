import pandas as pd
from fpdf import FPDF
import openai
import os
from datetime import datetime
from create_report_log import log_report
import streamlit as st

# Constants
INPUT_CSV = "parsed_trade_history.csv"
OUTPUT_PDF = "trade_report_output.pdf"
DEFAULT_LANGUAGE = "English"

# Supported languages
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Portuguese": "pt",
    "Spanish": "es",
    "Italian": "it",
    "Hindi": "hi",
    "Chinese": "zh",
    "Russian": "ru",
    "Arabic": "ar"
}

def load_trade_data(file_path):
    df = pd.read_csv(file_path)
    df = df[pd.to_numeric(df['Profit'], errors='coerce').notnull()]
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    return df

def compute_trade_stats(df):
    profits = df['Profit']
    total_profit = profits.sum()
    num_trades = len(profits)
    win_rate = (profits > 0).mean() * 100
    avg_profit = profits.mean()
    max_win = profits.max()
    max_loss = profits.min()
    return {
        "Total Profit": round(total_profit, 2),
        "Number of Trades": num_trades,
        "Win Rate": f"{win_rate:.2f}%",
        "Average Profit per Trade": round(avg_profit, 2),
        "Max Win": round(max_win, 2),
        "Max Loss": round(max_loss, 2)
    }

def generate_ai_feedback(stats, language_code="en"):
    prompt = f"""
    Act as a multilingual AI trading coach. Write a short feedback for a trader based on these stats:

    Total Profit: {stats['Total Profit']}
    Number of Trades: {stats['Number of Trades']}
    Win Rate: {stats['Win Rate']}
    Average Profit per Trade: {stats['Average Profit per Trade']}
    Max Win: {stats['Max Win']}
    Max Loss: {stats['Max Loss']}

    Be honest, motivational, educational. Short paragraph format.
    Respond in the language: {language_code}.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def create_pdf_report(stats, feedback, language=DEFAULT_LANGUAGE):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "📈 Trade Report Summary", ln=True)

    pdf.set_font("Arial", '', 12)
    for key, value in stats.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "GPT-4 Feedback:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, feedback)

    pdf.output(OUTPUT_PDF)
    print(f"📄 PDF saved as: {OUTPUT_PDF}")

def main():
    st.title("📊 AI Trade Evaluator")
    st.write("Upload your .csv or .xlsx trade file to get an AI-powered report.")

    language_choice = st.selectbox("🌍 Choose your language for the report:", list(LANGUAGES.keys()))
    language_code = LANGUAGES.get(language_choice, "en")

    uploaded_file = st.file_uploader("Choose file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df = df[pd.to_numeric(df['Profit'], errors='coerce').notnull()]
        df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')

        stats = compute_trade_stats(df)
        st.success("✅ File uploaded and stats computed!")
        st.write(stats)

        feedback = generate_ai_feedback(stats, language_code)
        st.write("🧠 GPT-4 Feedback:")
        st.info(feedback)

        create_pdf_report(stats, feedback, language=language_choice)
        log_report(stats, feedback)
        st.success("📄 PDF Report generated and saved!")

if __name__ == "__main__":
    main()
