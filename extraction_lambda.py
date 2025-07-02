import os
import json
import boto3
import requests
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize AWS S3 client and VADER analyzer
s3 = boto3.client('s3')
analyzer = SentimentIntensityAnalyzer()

def fetch_news():
    """Fetch top headlines from NewsAPI"""
    api_key = os.environ.get('api_key')  # Must be set in Lambda environment
    url = f'https://newsapi.org/v2/top-headlines?language=en&pageSize=100&sortBy=publishedAt&apiKey={api_key}'

    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def clean_text(text):
    """Clean whitespace and handle null strings"""
    if text is None:
        return None
    text = text.strip()
    return text if text else None

def format_date(date_str):
    """Format ISO date from NewsAPI"""
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%Y-%m-%dT%H-%M-%S")
    except ValueError:
        return None

def process_and_analyze_news(raw_data):
    """Clean and perform sentiment analysis on articles"""
    articles = raw_data.get('articles', [])
    processed = []

    sl_no = 1
    for article in articles:
        title = clean_text(article.get('title'))
        description = clean_text(article.get('description'))

        if not title or not description:
            continue  # skip invalid

        combined_text = f"{title} {description}".strip()
        sentiment = analyzer.polarity_scores(combined_text)

        processed.append({
            "S.No": sl_no,
            "VADER_Positive": sentiment['pos'],
            "VADER_Negative": sentiment['neg'],
            "VADER_Compound": sentiment['compound'],
            "Title": title,
            "Source": clean_text(article.get('source', {}).get('name')),
            "Description": description,
            "PublishedAt": format_date(article.get('publishedAt'))
        })

        sl_no += 1

    return processed

def upload_to_s3(data, bucket_name, folder="sentiment_data/"):
    """Upload sentiment-analyzed data to S3"""
    filename = f"news_sentiment_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.json"
    s3.put_object(
        Bucket=bucket_name,
        Key=folder + filename,
        Body=json.dumps(data, indent=2),
        ContentType='application/json'
    )

def lambda_handler(event, context):
    raw_news = fetch_news()
    processed_news = process_and_analyze_news(raw_news)

    if not processed_news:
        return {
            'statusCode': 204,
            'message': 'No valid articles to process.'
        }

    upload_to_s3(processed_news, bucket_name='mekhanewsdata')

    return {
        'statusCode': 200,
        'message': f'Successfully processed and uploaded {len(processed_news)} articles with sentiment analysis.'
    }
