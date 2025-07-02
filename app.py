import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# DB connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

# Query data
query = '''
    SELECT "S.No", "PublishedAt", "Source", "Title", "Sentiment"
    FROM news_sentiment
    ORDER BY "PublishedAt" DESC;
'''
df = pd.read_sql(query, conn)
conn.close()

# Highlight only the 'Sentiment' column
def highlight_sentiment_column(val):
    val = val.lower()
    if val == 'positive':
        return 'background-color: #006400; color: white'  # dark green
    elif val == 'negative':
        return 'background-color: #8B0000; color: white'  # dark red
    elif val == 'neutral':
        return 'background-color: #A9A9A9; color: black'  # dark gray
    return ''

# Column header styling
header_styles = [
    {'selector': 'th', 'props': [('font-weight', 'bold'), ('color', 'black')]}
]

# Apply both styles
styled_df = (
    df.style
    .applymap(highlight_sentiment_column, subset=['Sentiment'])
    .set_table_styles(header_styles)
)

# Display
st.title("🗞️ Sentiment News Table")
st.write("Showing latest sentiment-labeled news articles:")

st.dataframe(styled_df)
