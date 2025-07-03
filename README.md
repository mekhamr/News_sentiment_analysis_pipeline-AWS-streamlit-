# News_sentiment_analysis_pipeline-AWS-streamlit-
This project implements an end-to-end automated pipeline to fetch news articles, perform sentiment analysis, store results in a PostgreSQL RDS database, and visualize them using a Streamlit dashboard hosted on AWS ECS Fargate.
# Architecture
This architecture enables a real-time news sentiment analysis pipeline using AWS services. 
An EventBridge rule triggers a Lambda function every 5 minutes to fetch news articles from a News API. 
The Lambda function performs sentiment analysis using VADER and stores raw data in S3 and processed data in Amazon RDS (PostgreSQL).
A Dockerized Streamlit dashboard is pushed to Amazon ECR and deployed on ECS Fargate.

![Architecture](https://github.com/user-attachments/assets/9a7cfa60-f32f-4e8b-adeb-07ee4ecd3f60)

# 1.  Creating a News API : 
An API key was created using the NewsAPI website to fetch the latest news headlines for processing.
# 2. AWS  Lambda Function



