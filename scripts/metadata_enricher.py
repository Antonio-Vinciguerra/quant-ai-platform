import os
import json
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch

# === Paths ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(CURRENT_DIR, "../knowledge_base/cleaned")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "../processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load Models ===
print("🔍 Loading FinBERT and VADER...")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device set to use {device}")

tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone").to(device)
vader = SentimentIntensityAnalyzer()

# === FinBERT Inference ===
def analyze_sentiment(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment = torch.argmax(probs).item()
        labels = ["negative", "neutral", "positive"]
        return labels[sentiment], probs[0][sentiment].item()
    except Exception as e:
        print(f"[FinBERT ERROR] {e}")
        # fallback to VADER
        score = vader.polarity_scores(text)["compound"]
        if score >= 0.05:
            return "positive", score
        elif score <= -0.05:
            return "negative", abs(score)
        else:
            return "neutral", abs(score)

# === Process Articles ===
print("📚 Processing articles...")

data = []

if not os.path.exists(INPUT_DIR) or not os.listdir(INPUT_DIR):
    print(f"🚫 No files found in {INPUT_DIR}")
    exit(1)

for filename in tqdm(os.listdir(INPUT_DIR)):
    if filename.endswith(".json"):
        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, "r") as f:
            article = json.load(f)
            title = article.get("title", "")
            summary = article.get("summary", "")
            content = f"{title} {summary}"
            sentiment, score = analyze_sentiment(content)

            article["sentiment"] = sentiment
            article["sentiment_score"] = score
            data.append(article)

# === Save as Parquet ===
df = pd.DataFrame(data)
output_path = os.path.join(OUTPUT_DIR, "sentiment_enriched.parquet")
df.to_parquet(output_path, index=False)
print(f"✅ Enrichment complete: {len(df)} articles saved to {output_path}")
