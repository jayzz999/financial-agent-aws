import pandas as pd
from agents.summarization_agent import summarize_text

def generate_report(sentiment_results):
    # Extract data and normalize labels to lowercase
    data = []
    for title, result in sentiment_results:
        label = result['label'].lower()  # Convert to lowercase
        score = result['score']
        data.append((title, label, score))
    
    df = pd.DataFrame(data, columns=["title", "sentiment", "confidence"])
    
    # Debug: print unique sentiments to see what we're getting
    print(f"Unique sentiments: {df['sentiment'].unique()}")
    print(f"Sentiment counts:\n{df['sentiment'].value_counts()}")
    
    # Generate summary
    summary = summarize_text(" ".join(df['title'].tolist()[:20]))  # Use first 20 titles
    
    # Count sentiments
    report = {
        "summary": summary,
        "positive": df[df['sentiment'] == 'positive'].shape[0],
        "negative": df[df['sentiment'] == 'negative'].shape[0],
        "neutral": df[df['sentiment'] == 'neutral'].shape[0]
    }
    
    return report
