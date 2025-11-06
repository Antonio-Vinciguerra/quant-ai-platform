import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
from deep_translator import GoogleTranslator
import os

# Constants
OUTPUT_PDF = "trade_report.pdf"
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "fr": "French",
    "hi": "Hindi",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian"
}


def analyze_trades(df):
    try:
        if "Profit" not in df.columns:
            raise ValueError("❌ Your file does not have a column named 'Profit'. Please upload a valid trade file.")
        stats = {
            "Total Trades": len(df),
            "Profitable Trades": (df["Profit"] > 0).sum(),
            "Losing Trades": (df["Profit"] <= 0).sum(),
            "Win Rate": f"{round((df['Profit'] > 0).mean() * 100, 2)}%",
            "Average Profit": round(df["Profit"].mean(), 2),
            "Max Profit": df["Profit"].max(),
            "Max Loss": df["Profit"].min()
        }
        return stats, None
    except Exception as e:
        return None, str(e)


def generate_feedback(stats):
    if stats is None:
        return "No feedback: missing stats."
    feedback = []
    if stats["Win Rate"] < "50%":
        feedback.append("⚠️ Try to improve your win rate above 50%.")
    if stats["Average Profit"] < 0:
        feedback.append("📉 Your average profit is negative — revise your strategy.")
    if stats["Max Loss"] < -100:
        feedback.append("💥 Big losses detected. Use tighter stop losses.")
    return "\n".join(feedback) if feedback else "✅ Solid trading performance."


def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"(Translation error) {text}"


def create_pdf_report(stats, feedback, language_code):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    title = translate_text("AI Trade Evaluation Report", language_code)
    pdf.cell(200, 10, txt=title, ln=True, align='C')

    pdf.ln(10)
    for key, value in stats.items():
        label = translate_text(key, language_code)
        pdf.cell(200, 10, txt=f"{label}: {value}", ln=True)

    pdf.ln(10)
    pdf.multi_cell(200, 10, txt=translate_text("Feedback:", language_code))
    pdf.multi_cell(200, 10, txt=translate_text(feedback, language_code))

    pdf.output(OUTPUT_PDF)


def main():
    st.title("📊 AI Trade Evaluator")
    st.markdown("Upload your **trade history file** (.csv or .xlsx) and get an AI-generated PDF report.")

    uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx"])
    lang = st.selectbox("🌍 Select Report Language", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])

    if uploaded_file:
        # Load file
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.subheader("📄 Uploaded File Preview")
            st.dataframe(df.head())

            stats, error = analyze_trades(df)

            if error:
                st.error(error)
            else:
                feedback = generate_feedback(stats)

                st.subheader("📈 AI-Generated Stats")
                st.write(stats)

                st.subheader("💬 Feedback")
                st.info(feedback)

                if st.button("📄 Generate AI PDF Report"):
                    create_pdf_report(stats, feedback, lang)
                    with open(OUTPUT_PDF, "rb") as f:
                        st.download_button("⬇️ Download Report", f, file_name=OUTPUT_PDF)

        except Exception as e:
            st.error(f"❌ File processing error: {e}")


if __name__ == "__main__":
    main()
