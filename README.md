# News_sentiment_analysis_pipeline-AWS-streamlit-
This project implements an end-to-end automated pipeline to fetch news articles, perform sentiment analysis, store results in a PostgreSQL RDS database, and visualize them using a Streamlit dashboard hosted on AWS ECS Fargate.
# Architecture
![Architecture](https://github.com/user-attachments/assets/9a7cfa60-f32f-4e8b-adeb-07ee4ecd3f60)
# 1. News API : 
The application uses a News API to fetch the latest headlines. This API acts as the primary data source, delivering news articles in JSON format for processing.
# 2. AWS Lambda (Scheduled Task via EventBridge)
   # 1.a) Scheduled Trigger via EventBridge:
     An AWS Lambda function is scheduled to run every 5 minutes using Amazon EventBridge.
     
![img2](https://github.com/user-attachments/assets/03a209d2-e389-4aa9-bbe4-984272a5e7cf)



