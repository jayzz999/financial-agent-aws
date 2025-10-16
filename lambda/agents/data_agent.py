import os
import streamlit as st
from newsapi import NewsApiClient

def get_api_key():
    """Get News API key from Streamlit secrets or environment"""
    try:
        return st.secrets["NEWS_API_KEY"]
    except:
        return os.getenv("NEWS_API_KEY", "dafe67207d044b2abfa9aaa1bae3e7c5")

def fetch_news(query="stock market", max_articles=50):
    newsapi = NewsApiClient(api_key=get_api_key())
    all_articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=max_articles)
    return [(a['title'], a['description']) for a in all_articles['articles']]

if __name__ == "__main__":
    news = fetch_news()
    print(news[:5])
