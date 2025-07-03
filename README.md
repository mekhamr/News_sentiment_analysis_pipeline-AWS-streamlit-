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
# 2. Fetches news articles from an API every 5 minutes and analyzes the sentiment of each article using VADER.
An AWS EventBridge rule triggers a Lambda function every 5 minutes to ensure the news data is refreshed regularly. The Lambda function fetches the latest news articles from a News API, performs sentiment analysis using the VADER NLP model, and stores the raw articles in Amazon S3 in JSON format. Amazon S3 acts as a backup storage location for the raw data, useful for audits or future retraining. This setup ensures continuous, automated collection and analysis of news data in near real-time.

![img1](https://github.com/user-attachments/assets/3eb3f998-2d88-4355-8e14-fcdd2400ae9a)
![img3](https://github.com/user-attachments/assets/31ab2132-b016-409e-996f-7337d724d6ec)

# 3. Inserting Sentiment Data into Amazon RDS 
This Lambda function handles the transfer of sentiment-analyzed news articles from Amazon S3 to Amazon RDS (PostgreSQL). It begins by connecting to the database using credentials stored in environment variables and ensures the target table (news_sentiment) exists with a unique "S.No" field to avoid duplicates. Each article is parsed, its timestamp is formatted, and sentiment is determined using the VADER compound score before inserting into the database. After successful processing, the corresponding S3 files are deleted to prevent reprocessing in future Lambda executions.

![img8](https://github.com/user-attachments/assets/ce759069-5ca0-4ba2-ae5d-bd8009d5ea4c)
![img17](https://github.com/user-attachments/assets/42de3ae4-9857-4482-9884-2014ede09c1c)

# 4.  visualise the streamlit dashboard locally
A real-time dashboard was developed using Streamlit to visualize sentiment-labeled news articles stored in Amazon RDS (PostgreSQL). The dashboard displays headlines in a clean tabular format with color-coded sentiment labels (green for positive, red for negative, gray for neutral).

![Screenshot (160)](https://github.com/user-attachments/assets/a8aa3087-8b5d-43d2-b91e-a6dd52d9346b)

![Screenshot (161)](https://github.com/user-attachments/assets/067524eb-ccdc-42be-abfb-2577ec113563)

# 5. The Streamlit dashboard is containerized using Docker, and the image is pushed to Amazon ECR.
![img9](https://github.com/user-attachments/assets/91e4be79-52dd-4bce-b76c-8d6fccbc83df)

![img12](https://github.com/user-attachments/assets/74070783-82c3-4c2b-9f3e-306753567e1a)

# 6. Deployed on ECS
The Docker image is deployed on an AWS Fargate cluster by creating a task definition that specifies the container settings. Once the task is running, the public IP and assigned port can be used to access the Streamlit dashboard directly from a browser. This setup allows serverless, scalable, and real-time visualization of sentiment-analyzed news data.
![img13](https://github.com/user-attachments/assets/a95f9b83-1c37-4d78-b6aa-ebde46c291cc)

![img14](https://github.com/user-attachments/assets/3811ef93-b8b1-45e4-a1ef-b7f4280a16a4)

![img15](https://github.com/user-attachments/assets/1d3aff4f-b28c-47f5-ad7e-72a37ea7e544)

![img18](https://github.com/user-attachments/assets/5e89d884-4947-4a9c-bf68-922233b2194f)











