import pandas as pd
import re
from unidecode import unidecode
import spacy
import nltk
from nltk.stem import SnowballStemmer

df = pd.read_csv('argentine_tweets.csv', encoding = 'UTF-8')
tweets = df['Text']

def remove_re(spanish_tweets):
    tweets_without_re = []
    for sentence in spanish_tweets:
        processed_text = re.sub(r'https\S+', '', sentence) 
        processed_text = re.sub(r'\W', ' ', processed_text)
        processed_text = re.sub(r'(.)\1{2,}', r'\1', processed_text)
        processed_text = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_text)
        processed_text = re.sub(r'\s+', ' ', processed_text)
        processed_text = re.sub('ñ', 'gn', processed_text)
        processed_text = unidecode(processed_text.lower())
        tweets_without_re.append(processed_text)
    return (tweets_without_re)

def normalize_tweets(spanish_tweets):
    nlp = spacy.load('es_core_news_sm')
    tok = [nlp(word) for word in spanish_tweets]
    lemma = []
    for sentence in tok:
        for token in sentence:
            if token.is_stop == False:
                lemma.append(token.lemma_)
    stemmer = SnowballStemmer('spanish')
    normalized_tweets = [stemmer.stem(token) for token in lemma]
    return normalized_tweets



