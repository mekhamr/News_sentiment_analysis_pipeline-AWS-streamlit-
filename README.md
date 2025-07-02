# News_sentiment_analysis_pipeline-AWS-streamlit-
This project implements an end-to-end automated pipeline to fetch news articles, perform sentiment analysis, store results in a PostgreSQL RDS database, and visualize them using a Streamlit dashboard hosted on AWS ECS Fargate.
# Architecture
![Architecture](https://github.com/user-attachments/assets/9a7cfa60-f32f-4e8b-adeb-07ee4ecd3f60)
# 1. News API : 
An API key was created using the NewsAPI website to fetch the latest news headlines for processing.
# 2. AWS Lambda 
# a) first lambda function
The Lambda function fetches the latest news articles from the News API during each scheduled run.
![Screenshot (135)](https://github.com/user-attachments/assets/ae97a2e1-65f5-4b82-ac02-6efb745c1dfd)


   # 1.a) Scheduled Trigger via EventBridge:
     An AWS Lambda function is scheduled to run every 5 minutes using Amazon EventBridge.
     
![img2](https://github.com/user-attachments/assets/03a209d2-e389-4aa9-bbe4-984272a5e7cf)



