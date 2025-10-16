def generate_report(sentiment_results):
    """Generate report from sentiment results - Lambda version"""
    
    # Count sentiments
    positive = 0
    negative = 0
    neutral = 0
    
    titles = []
    for title, result in sentiment_results:
        label = result['label'].lower()
        titles.append(title)
        
        if label == 'positive':
            positive += 1
        elif label == 'negative':
            negative += 1
        else:
            neutral += 1
    
    # Simple summary (you can use OpenAI here if you want)
    total = len(sentiment_results)
    summary = f"Analyzed {total} articles. "
    
    if positive > negative:
        summary += f"Overall sentiment is POSITIVE ({positive}/{total} articles). "
    elif negative > positive:
        summary += f"Overall sentiment is NEGATIVE ({negative}/{total} articles). "
    else:
        summary += f"Market sentiment is MIXED. "
    
    summary += f"Top headlines: {', '.join(titles[:3])}"
    
    return {
        "summary": summary,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "total": total,
        "top_headlines": titles[:5]
    }