# News_sentiment_analysis_pipeline-AWS-streamlit-
This project implements an end-to-end automated pipeline to fetch news articles, perform sentiment analysis, store results in a PostgreSQL RDS database, and visualize them using a Streamlit dashboard hosted on AWS ECS Fargate.
# Architecture
![Architecture](https://github.com/user-attachments/assets/9a7cfa60-f32f-4e8b-adeb-07ee4ecd3f60)
# 1. News API : 
The application uses a News API to fetch the latest headlines. This API acts as the primary data source, delivering news articles in JSON format for processing.
# 2. AWS Lambda (Scheduled Task via EventBridge)
  1.a) Scheduled Trigger via EventBridge
       An AWS Lambda function is scheduled to run every 5 minutes using Amazon EventBridge.
      ![img2](https://github.com/user-attachments/assets/03a209d2-e389-4aa9-bbe4-984272a5e7cf)


🧠 2. Fetch News Articles from API
The Lambda function fetches the latest news articles from the News API during each scheduled run.
📸 (Add image of API call or globe + document symbol here)

🗣️ 3. Sentiment Analysis using VADER
The text of each news article is analyzed using the VADER (Valence Aware Dictionary for Sentiment Reasoning) model from the NLTK library to determine whether it's positive, negative, or neutral.
📸 (Insert icon: magnifying glass with smile/sad/neutral emoji, or NLTK + VADER illustration)

💾 4. Store Raw Data in Amazon S3
Before processing, raw JSON data is saved to an Amazon S3 bucket for backup and auditing purposes.
📸 (Add image of S3 bucket with .json file or folder icon here)

🗃️ 5. Store Cleaned Data in Amazon RDS
The sentiment-labeled articles are stored in a structured format in a PostgreSQL database hosted on Amazon RDS.
📸 (Insert icon: PostgreSQL elephant + AWS RDS logo here)
