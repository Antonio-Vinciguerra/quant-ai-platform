import os
import openai
import streamlit as st
from dotenv import load_dotenv

# === Load secrets ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Model cost mapping (you can adjust this) ===
MODEL_COST = {
    "gpt-3.5-turbo": 0.001,     # USD per 1K tokens (adjust as needed)
    "gpt-4": 0.03,
    "gpt-4-1106-preview": 0.01,  # Example cost if using GPT-4 Turbo
}

# === App Config ===
st.set_page_config(page_title="QuantMentor X Chat", layout="wide")
st.title("🧠 QuantMentor X - Multi-Model Chat")
st.markdown("This assistant supports multiple models with live cost tracking 💸")

# === Session State Initialization ===
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.total_tokens = 0
    st.session_state.total_cost = 0.0

# === Sidebar Model Selector ===
st.sidebar.header("Model Settings")
selected_model = st.sidebar.selectbox("Choose model", list(MODEL_COST.keys()))
cost_per_1k = MODEL_COST[selected_model]

# === Chat Display ===
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# === User Input ===
prompt = st.chat_input("Ask your trading mentor anything...")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        client = openai.Client()
        response = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # === Token usage tracking ===
        tokens_used = response.usage.total_tokens
        st.session_state.total_tokens += tokens_used
        st.session_state.total_cost += (tokens_used / 1000) * cost_per_1k

# === Usage Summary ===
st.sidebar.markdown("---")
st.sidebar.metric("📊 Total Tokens", f"{st.session_state.total_tokens}")
st.sidebar.metric("💵 Total Cost (USD)", f"${st.session_state.total_cost:.4f}")
