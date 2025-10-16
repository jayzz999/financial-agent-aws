import os
import requests
import time

def analyze_sentiment_huggingface(text):
    """Use HuggingFace Inference API - ProsusAI/finbert model"""
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    
    if not api_key:
        return None
    
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.post(
            API_URL, 
            headers=headers, 
            json={"inputs": text},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            # Model loading, retry once
            time.sleep(20)
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=30)
            if response.status_code == 200:
                return response.json()
        return None
            
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None

def analyze_sentiment(news_list):
    """Analyze sentiment for list of news"""
    results = []
    
    for title, desc in news_list:
        try:
            result = analyze_sentiment_huggingface(title)
            
            if result and isinstance(result, list) and len(result) > 0:
                sentiments = result[0] if isinstance(result[0], list) else result
                top_sentiment = sentiments[0]
                
                results.append((title, {
                    'label': top_sentiment['label'],
                    'score': top_sentiment['score']
                }))
            else:
                results.append((title, {'label': 'neutral', 'score': 0.5}))
                
        except Exception as e:
            print(f"Error processing article: {e}")
            results.append((title, {'label': 'neutral', 'score': 0.5}))
    
    return results
