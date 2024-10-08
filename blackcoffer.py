# -*- coding: utf-8 -*-
"""BLACKCOFFER.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17STf9rHqOaEpYuXSjTnjq30oW0ZSOela

# Installing required libraries
"""

pip install pandas requests beautifulsoup4 nltk

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize

"""# Loading of excel file"""

# Load the Excel file
input_file = "/content/Input.xlsx"
df = pd.read_excel(input_file)

# Function to extract text from the URL
def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Assuming that the article title is in <h1> and the text in <p> tags
        title = soup.find('h1').get_text(strip=True)
        paragraphs = soup.find_all('p')
        article_text = '\n'.join([para.get_text(strip=True) for para in paragraphs])

        return title + '\n' + article_text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Directory to save the extracted articles
output_dir = 'extracted_articles'
os.makedirs(output_dir, exist_ok=True)

# Iterate over each URL and save the article text
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    article_text = extract_article_text(url)

    if article_text:
        with open(f'{output_dir}/{url_id}.txt', 'w', encoding='utf-8') as f:
            f.write(article_text)

# Download required nltk data
nltk.download('vader_lexicon')
nltk.download('punkt')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Function to compute text analysis metrics
def analyze_text(article_text):
    # Calculate Positive, Negative, Polarity, and Subjectivity Scores
    sentiment_scores = sia.polarity_scores(article_text)
    positive_score = sentiment_scores['pos']
    negative_score = sentiment_scores['neg']
    polarity_score = sentiment_scores['compound']
    subjectivity_score = (positive_score + negative_score) / (len(article_text.split()) + 1e-6)

    # Sentence and word counts
    sentences = sent_tokenize(article_text)
    words = word_tokenize(article_text)

    avg_sentence_length = len(words) / len(sentences)
    complex_words = [word for word in words if len(word) > 6]  # Example of complex words
    percentage_complex_words = len(complex_words) / len(words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = avg_sentence_length

    # Other metrics
    complex_word_count = len(complex_words)
    word_count = len(words)
    syllable_per_word = sum([len(word) // 2 for word in words]) / len(words)  # Simplified example
    personal_pronouns = len([word for word in words if word.lower() in ['i', 'we', 'my', 'ours', 'us']])
    avg_word_length = sum([len(word) for word in words]) / len(words)

    return {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "polarity_score": polarity_score,
        "subjectivity_score": subjectivity_score,
        "avg_sentence_length": avg_sentence_length,
        "percentage_complex_words": percentage_complex_words,
        "fog_index": fog_index,
        "avg_words_per_sentence": avg_words_per_sentence,
        "complex_word_count": complex_word_count,
        "word_count": word_count,
        "syllable_per_word": syllable_per_word,
        "personal_pronouns": personal_pronouns,
        "avg_word_length": avg_word_length
    }

# Apply the analysis to all extracted articles
output_data = []

for index, row in df.iterrows():
    url_id = row['URL_ID']
    with open(f'{output_dir}/{url_id}.txt', 'r', encoding='utf-8') as f:
        article_text = f.read()

    analysis_results = analyze_text(article_text)
    output_data.append({**row, **analysis_results})

# Convert results to DataFrame
output_df = pd.DataFrame(output_data)

# Save the results to Excel
output_file = "Output_Data_Structure.xlsx"
output_df.to_excel(output_file, index=False)

# Download required nltk data
nltk.download('vader_lexicon')
nltk.download('punkt')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

"""# Function to find positive_score, negative_score, polarity_score, subjectivity_score"""

def sentiment_scores(article_text):
    # Calculate Positive, Negative, Polarity, and Subjectivity Scores
    sentiment = sia.polarity_scores(article_text)
    positive_score = sentiment['pos']
    negative_score = sentiment['neg']
    polarity_score = sentiment['compound']
    subjectivity_score = (positive_score + negative_score) / (len(article_text.split()) + 1e-6)

    return positive_score, negative_score, polarity_score, subjectivity_score

"""# Function to find the avg sentence length , complex words , fogindex etc"""

def sentence_word_analysis(article_text):
    sentences = sent_tokenize(article_text)
    words = word_tokenize(article_text)

    avg_sentence_length = len(words) / len(sentences)
    complex_words = [word for word in words if len(word) > 6]  # Example of complex words
    percentage_complex_words = len(complex_words) / len(words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = avg_sentence_length

    return avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, len(complex_words), len(words)

"""# Function to find the additional metrics

"""

def additional_metrics(words):
    syllable_per_word = sum([len(word) // 2 for word in words]) / len(words)  # Simplified example
    personal_pronouns = len([word for word in words if word.lower() in ['i', 'we', 'my', 'ours', 'us']])
    avg_word_length = sum([len(word) for word in words]) / len(words)

    return syllable_per_word, personal_pronouns, avg_word_length

"""# Analyzing the text"""

def analyze_text(article_text):
    positive_score, negative_score, polarity_score, subjectivity_score = sentiment_scores(article_text)
    avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count = sentence_word_analysis(article_text)
    words = word_tokenize(article_text)
    syllable_per_word, personal_pronouns, avg_word_length = additional_metrics(words)

    return {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "polarity_score": polarity_score,
        "subjectivity_score": subjectivity_score,
        "avg_sentence_length": avg_sentence_length,
        "percentage_complex_words": percentage_complex_words,
        "fog_index": fog_index,
        "avg_words_per_sentence": avg_words_per_sentence,
        "complex_word_count": complex_word_count,
        "word_count": word_count,
        "syllable_per_word": syllable_per_word,
        "personal_pronouns": personal_pronouns,
        "avg_word_length": avg_word_length
    }

"""# storing the data in the output file"""

output_data = []

for index, row in df.iterrows():
    url_id = row['URL_ID']
    with open(f'{output_dir}/{url_id}.txt', 'r', encoding='utf-8') as f:
        article_text = f.read()

    analysis_results = analyze_text(article_text)
    output_data.append({**row, **analysis_results})

# Convert results to DataFrame
output_df = pd.DataFrame(output_data)

# Save the results to Excel
output_file = "Output_Data_Structure.xlsx"
output_df.to_excel(output_file, index=False)

output_df.head(10)

"""# Running commands"""

THIS IS A GOOGLE COLOB FILE IF YOU WISH TO RUN THIS
YOU WANT TO INSTALL THE NECESSARY MODULES RELATED TO THE GOOGLE
COLAB.AND USING THE RUN OPTION IN THE COLAB...
with open('Output_Data_Structure.xlsx', 'a') as f:#creating text file
    output.to_csv(f, index=False, header=False)
files.download('output_Data_Structure.csv')







