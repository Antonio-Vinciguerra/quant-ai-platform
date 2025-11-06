# ai_feedback.py

from deep_translator import GoogleTranslator
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_feedback(stats, language='en'):
    # Prepare a basic English prompt
    prompt = (
        f"Generate a trading performance analysis based on these stats:\n"
        f"Total Profit: {stats['Total Profit']}\n"
        f"Number of Trades: {stats['Number of Trades']}\n"
        f"Win Rate: {stats['Win Rate']}\n"
        f"Average Profit per Trade: {stats['Average Profit per Trade']}\n"
        f"Max Win: {stats['Max Win']}\n"
        f"Max Loss: {stats['Max Loss']}\n"
    )

    # Call GPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional trading coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    english_feedback = response['choices'][0]['message']['content'].strip()

    # Translate if needed
    if language != 'en':
        try:
            translated = GoogleTranslator(source='en', target=language).translate(english_feedback)
            return translated
        except Exception as e:
            return f"⚠️ Translation failed, showing English:\n\n{english_feedback}"
    else:
        return english_feedback
