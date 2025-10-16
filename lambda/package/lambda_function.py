import json
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from data_agent_lambda import fetch_news
from sentiment_agent_lambda import analyze_sentiment
from report_agent_lambda import generate_report

def lambda_handler(event, context):
    """
    AWS Lambda handler for financial agent
    
    Expected input:
    {
        "query": "stock market",
        "max_articles": 20
    }
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse input
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        query = body.get('query', 'stock market')
        max_articles = body.get('max_articles', 20)
        
        print(f"Fetching news for: {query}")
        
        # Step 1: Fetch news
        news = fetch_news(query=query, max_articles=max_articles)
        print(f"Fetched {len(news)} articles")
        
        if not news:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': True,
                    'message': 'No articles found',
                    'report': {
                        'positive': 0,
                        'negative': 0,
                        'neutral': 0
                    }
                })
            }
        
        # Step 2: Analyze sentiment
        print("Analyzing sentiment...")
        sentiments = analyze_sentiment(news[:10])  # Limit to 10 for speed
        print(f"Analyzed {len(sentiments)} articles")
        
        # Step 3: Generate report
        print("Generating report...")
        report = generate_report(sentiments)
        
        print("Report generated successfully!")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'query': query,
                'articles_analyzed': len(sentiments),
                'report': report
            }, indent=2)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }

# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        "query": "Tesla stock",
        "max_articles": 5
    }
    
    result = lambda_handler(test_event, None)
    print("\nTest Result:")
    print(result['body'])
