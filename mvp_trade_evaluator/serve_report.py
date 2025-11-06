import streamlit as st
import base64
import os

# Set your report path
PDF_PATH = "trade_report_output.pdf"

# Page config
st.set_page_config(page_title="Trade Report Viewer", layout="centered")

st.title("📄 Trade Report Viewer")

if os.path.exists(PDF_PATH):
    st.success("✅ PDF report generated successfully!")

    with open(PDF_PATH, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    st.download_button(
        label="⬇️ Download Report",
        data=open(PDF_PATH, "rb"),
        file_name="trade_report_output.pdf",
        mime="application/pdf"
    )
else:
    st.error("❌ PDF report not found. Please generate it first.")
