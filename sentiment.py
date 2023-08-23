# -*- coding: utf-8 -*-
"""Sentiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YeRInTdLbF_6LzqAhdS9YBNsOb3c7YcN
"""

!pip install nltk
import nltk

nltk.download('vader_lexicon')

import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Define the URL for fetching Reddit comments
reddit_api_url = "https://api.pullpush.io/reddit/search/comment/?q=toyota&before=1680303707"

# Initialize counters for sentiment categories
positive_count = 0
neutral_count = 0
negative_count = 0

# Number of comments to analyze (adjust as needed)
num_comments_to_analyze = 10000

# Make API requests to fetch comments
while num_comments_to_analyze > 0:
    response = requests.get(reddit_api_url)
    if response.status_code != 200:
        print("Error fetching Reddit comments.")
        break

    data = response.json()
    comments = data["data"]

    for comment in comments:
        comment_text = comment["body"]

        # Perform sentiment analysis
        sentiment = sia.polarity_scores(comment_text)

        # Classify sentiment
        if sentiment["compound"] >= 0.05:
            positive_count += 1
        elif sentiment["compound"] <= -0.05:
            negative_count += 1
        else:
            neutral_count += 1

        num_comments_to_analyze -= 1

    # Update the 'before' parameter to get more comments
    if comments:
        last_created_utc = comments[-1]["created_utc"]
        reddit_api_url = f"https://api.pullpush.io/reddit/search/comment/?q=toyota&before={last_created_utc - 1}"

# Print the results
print("Sentiment Analysis Results:")
print(f"Positive Comments: {positive_count}")
print(f"Neutral Comments: {neutral_count}")
print(f"Negative Comments: {negative_count}")

!pip install vaderSentiment

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Custom threshold values
positive_threshold = 0.2
negative_threshold = -0.2

# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Add more preprocessing steps as needed
    return text

# Function to get Reddit comments
def get_reddit_comments(before_timestamp):
    url = f"https://api.pullpush.io/reddit/search/comment/?q=toyota&before={before_timestamp}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return []

# Function to perform sentiment analysis and return the result
def analyze_sentiment(comments):
    results = []
    for comment in comments:
        text = comment["body"]
        text = preprocess_text(text)  # Preprocess the text
        sentiment_scores = analyzer.polarity_scores(text)
        # Smooth the scores
        compound_score = sentiment_scores["compound"]
        if compound_score > 1.0:
            compound_score = 1.0
        elif compound_score < -1.0:
            compound_score = -1.0
        # Apply custom thresholds
        if compound_score >= positive_threshold:
            sentiment = "Positive"
        elif compound_score <= negative_threshold:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        result = f"{text},{sentiment_scores['pos']},{sentiment_scores['neu']},{sentiment_scores['neg']},{sentiment}"
        results.append(result)
    return results

# Main function to fetch comments and analyze sentiment
def main():
    num_comments = 10000  # Number of comments to analyze
    before_timestamp = 1680303707  # Initial timestamp

    while num_comments > 0:
        comments = get_reddit_comments(before_timestamp)
        if not comments:
            break

        results = analyze_sentiment(comments)
        for result in results:
            print(result)

        # Update the timestamp for the next batch
        before_timestamp = comments[-1]["created_utc"] - 1
        num_comments -= len(comments)

if __name__ == "__main__":
    main()

