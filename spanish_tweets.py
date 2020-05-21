import tweepy
from tweepy import Cursor
import json
import time
import pandas as pd

# API authenticating

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Function to get tweets

def get_spanish_tweets(country, keyword, count):
    corpus = {}
    tweet_count = 0

    try:
        place = api.geo_search(query=country, granulaty='country')
        place_id = place[0].id
    except IndexError:
        place_id = None

    while tweet_count != count:
        try:
            tweets = Cursor(api.search, 
                            q=keyword, 
                            place=place_id, 
                            lang='es', 
                            include_entities=True, 
                            tweet_mode='extended').items(count)
            for tweet in tweets:
                tweet = tweet._json
                corpus.setdefault('Id', []).append(tweet['id'])
                corpus.setdefault('Date', []).append(tweet['created_at'])
                corpus.setdefault('User', []).append(tweet['user']['screen_name'])
                corpus.setdefault('User_fallowers', []).append(tweet['user']['followers_count'])
                corpus.setdefault('Text', []).append(tweet['full_text'])
                corpus.setdefault('Hashtags', []).append(tweet['entities']['hashtags'])
                tweet_count += 1
        except tweepy.TweepError:
            time.sleep(900)
            continue

    corpus_pd = pd.DataFrame({key:pd.Series(value) for key, value in corpus.items()})
    return corpus_pd.to_csv(r'.\argentine_tweets.csv', index=False)
