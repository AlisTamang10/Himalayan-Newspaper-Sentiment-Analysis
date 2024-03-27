import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import subprocess
import time

def download_model_with_retry():
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            # Attempt to download the model
            tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
            model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
            return tokenizer, model
        except Exception as e:
            print(f"Error downloading model: {e}")
            retries += 1
            print(f"Retrying ({retries}/{max_retries})...")
            time.sleep(2)  # Wait for 2 seconds before retrying
    raise RuntimeError("Failed to download model after multiple retries")

def sentiment_analysis_function(text):
    # Install Model
    tokenizer, model = download_model_with_retry()

    # Check if the text is empty or not 
    if not text or not isinstance(text,str):
        return 0, "Invalid Text"

    # Tokenize and analyze sentiment
    tokens = tokenizer.encode(text, return_tensors='pt',max_length=512, truncation=True)
    result = model(tokens)

    # Apply softmax 
    probabilities = torch.softmax(result.logits, dim=1)

    # Get the sentiment score and label
    sentiment_score = int(torch.argmax(probabilities)) + 1

    # Determine sentiment label
    if sentiment_score >= 4:
        sentiment_label = "Positive"
    elif sentiment_score == 3:
        sentiment_label = "Neutral"
    else:
        sentiment_label = "Negative"

    return sentiment_score, sentiment_label

# Load the merged csv file into pandas DataFrame
df_a = pd.read_csv('Jimalayn_time_data.csv')

# Apply sentiment analysis to the Heading and Content columns
def apply_sentiment_analysis(row):
    heading_text = row['Heading']
    content_text = row['content']

    heading_sentiment_score, heading_sentiment_label = sentiment_analysis_function(heading_text)
    content_sentiment_score, content_sentiment_label = sentiment_analysis_function(content_text)

    print("Heading:", heading_text)
    print("Heading Sentiment Score:", heading_sentiment_score)
    print("Heading Sentiment Label:", heading_sentiment_label)
    print("Content:", content_text)
    print("Content Sentiment Score:", content_sentiment_score)
    print('Content Sentiment Label:', content_sentiment_label)
    print()  # Newline

    row['HeadingSentimentScore'] = heading_sentiment_score
    row['HeadingSentimentLabel'] = heading_sentiment_label
    row['ContentSentimentScore'] = content_sentiment_score
    row['ContentSentimentLabel'] = content_sentiment_label

    return row

# Apply Sentiment analysis to the dataframe
df_a_with_sentiment = df_a.apply(apply_sentiment_analysis, axis=1)

# Save the dataframe with sentiment analysis to new csv file
df_a_with_sentiment.to_csv('all_csv_with_sentiment.csv', index=False)
