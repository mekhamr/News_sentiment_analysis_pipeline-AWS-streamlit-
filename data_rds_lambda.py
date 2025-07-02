import json
import boto3
import psycopg2
import os
from datetime import datetime

# RDS credentials from environment variables
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

bucket_name = 'mekhanewsdata'
prefix = 'sentiment_data/'

# Initialize S3 client
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Ensure table exists (must already include "S.No")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news_sentiment (
                id SERIAL PRIMARY KEY,
                "S.No" INT UNIQUE,
                "PublishedAt" TIMESTAMP,
                "Source" TEXT,
                "Title" TEXT,
                "Sentiment" VARCHAR(10)
            );
        """)
        conn.commit()

        # Get max S.No
        cur.execute('SELECT COALESCE(MAX("S.No"), 0) FROM news_sentiment')
        s_no_counter = cur.fetchone()[0] + 1

        # List JSON files
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' not in response:
            return {"statusCode": 200, "message": "No files to process."}

        for obj in response['Contents']:
            key = obj['Key']
            if not key.endswith('.json'):
                continue

            # Load JSON
            s3_obj = s3.get_object(Bucket=bucket_name, Key=key)
            data = json.loads(s3_obj['Body'].read().decode('utf-8'))

            for row in data:
                raw_date = row.get("PublishedAt", None)
                published_at = None

                if raw_date:
                    try:
                        published_at = datetime.strptime(raw_date, "%Y-%m-%dT%H-%M-%S")
                    except Exception:
                        published_at = None

                source = row.get("Source", "")
                title = row.get("Title", "")
                compound = row.get("VADER_Compound", 0.0)

                if compound >= 0.05:
                    sentiment = 'positive'
                elif compound <= -0.05:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'

                # Insert with S.No
                cur.execute("""
                    INSERT INTO news_sentiment ("S.No", "PublishedAt", "Source", "Title", "Sentiment")
                    VALUES (%s, %s, %s, %s, %s)
                """, (s_no_counter, published_at, source, title, sentiment))

                s_no_counter += 1

            conn.commit()

            # Delete file after processing
            s3.delete_object(Bucket=bucket_name, Key=key)

        cur.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': 'Data inserted with S.No and files processed successfully.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
