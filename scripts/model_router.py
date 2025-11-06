# model_router.py

import os
import openai
from dotenv import load_dotenv

# Load .env variables
load_dotenv(dotenv_path=os.path.expanduser('~/quant-ai-platform/.env'))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

openai.api_key = OPENAI_API_KEY

def query_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("⚠️ OpenAI failed:", e)
        return None

def query_model(prompt):
    print("⚙️ Using OpenAI GPT-4...")
    return query_openai(prompt)

if __name__ == "__main__":
    prompt = input("🔹 Enter your question: ")
    answer = query_model(prompt)
    print("\n✅ Answer:\n", answer or "❌ GPT-4 failed.")
