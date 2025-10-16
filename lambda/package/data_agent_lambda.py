import os
import requests

def fetch_news(query="stock market", max_articles=50):
    """Fetch news from NewsAPI - Lambda version"""
    api_key = os.environ.get('NEWS_API_KEY')
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': max_articles,
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)
    articles = response.json().get('articles', [])
    
    return [(a['title'], a['description']) for a in articles if a['title']]