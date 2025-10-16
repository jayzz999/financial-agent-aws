import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    """Load summarization model once and cache it"""
    return pipeline("summarization")

def summarize_text(text):
    """Summarizes input text using Hugging Face local model."""
    summarizer = load_summarizer()
    
    max_chunk = 500
    if len(text) > max_chunk:
        text = text[:max_chunk]
    
    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]['summary_text']

if __name__ == "__main__":
    sample_text = "Stocks rise. Market positive sentiment. Tech leading the rally today in Nasdaq. Investors optimistic."
    summary = summarize_text(sample_text)
    print("Summary:", summary)
