import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

@st.cache_resource
def load_finbert():
    """Load FinBERT model once and cache it"""
    tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentiment(news_list):
    finbert = load_finbert()
    return [(title, finbert(title)[0]) for title, desc in news_list]

if __name__ == "__main__":
    sample_news = [("Stocks soar today", ""), ("Market crashes", "")]
    results = analyze_sentiment(sample_news)
    print(results)
