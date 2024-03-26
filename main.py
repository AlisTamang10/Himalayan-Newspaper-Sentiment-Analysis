import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import subprocess

def sentiment_analysis_function(text):
    #Install MOdel
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    
    #check if the text is empty or not 
    
    if not text or not isinstance(text,str):
        return 0, "Invalid Text"
    
    #Tokenize and analyze sentiment
    
    tokens = tokenizer.encode(text, return_tensors='pt',max_length=512, truncation=True)
    result = model(tokens)
    
    #apply softmax 
    probabilities = torch.softmax(result.logits, dim = 1)
    
    #get the sentiment score and label
    
    sentiment_score = int(torch.argmax(probabilities)) + 1
    
    #determine sentiment label
    
    if sentiment_score >=4:
        sentiment_label = "Positive"
        
    elif sentiment_score == 3:
        sentiment_label = "Neutral"
    else:
        sentiment_label = "Negative"
        
    return sentiment_score, sentiment_label
    
    #Execute Scripts for different news source
    
    
    
    
    #Load the merged csv file into pandas DataFrame
    
df_a = pd.read_csv('Jimalayn_time_data.csv')
    
    #apply sentiment analyssis to the Heading and Content columns
    
def apply_sentiment_analysis(row):
    
    heading_text = row['Heading']
    content_text = row['Content']
        
    heading_sentiment_score, heading_sentiment_label = sentiment_analysis_function(heading_text)
    content_sentiment_score, content_sentiment_label = sentiment_analysis_function(content_text)
        
    print("heading:", heading_text)
    print("Heading Sentiment Score:", heading_sentiment_score)
    print("Heading Sentiment Label:",heading_sentiment_label)
    print("content:", content_text)
    print("content sentiment score:", content_sentiment_score)
    print('content sentiment label:', content_sentiment_label)
    print() #newline
    
    row['HeadingSentimentScore'] = heading_sentiment_score     
     





