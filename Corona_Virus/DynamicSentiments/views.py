from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import os
import tweepy as tw
import pandas as pd
import numpy as np

from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

# Create your views here.


def Dysearch(request):
    print(request.GET)
    return render(request, 'dynamic_sentiment_search.html')


def Dysearch_output(request):
    query = request.GET['search']
    a = query
    query = "\"" + query + "\""
    data = get_tweets(query)
    print(data)
    data = classifying_positive_negative_1(data)
    
    return render(request, 'dynamic_sentiments.html', {'data_top': data.head(n=10), 'data_bottom': data.tail(n=10),'a': a})


def get_tweets(a):
    consumer_key = '0OXA7QU4jqoInCMCyJZaneHsE'
    consumer_secret = 'dDDGRta6UJ24k9CQG9v088VXawLgEX3czvY1EKriIIPgT1RW95'
    access_token = '1236865060544212993-72bAPQdeMpXoc6MPchsBAkvCzZRGDT'
    access_token_secret = '4bWJoY6yemqoG13Cb9bV6rX1nBrIqvt0I5gNxXwIqMuip'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    collection = pd.DataFrame(
        columns=['keyword', 'id', 'tweet', 'date', 'location', 'retweets', 'likes'])

    keyword = a
    number = 50

    try:
        tweets = tw.Cursor(api.search,
                           q=keyword,
                           lang="en", tweet_mode='extended').items(number)
    except:
        return collection

    for x in tweets:
        if(x.is_quote_status == False and x.retweeted == False):
            print(x.created_at)
            row = {'keyword': keyword,
                   'id': x._json['id'],
                   'tweet': x._json['full_text'],
                   'date': x._json['created_at'],
                   'location': x._json['place'],
                   'retweets': x._json['retweet_count'],
                   'likes': x._json['favorite_count']}
            collection = collection.append(row, ignore_index=True)

    return collection

def classifying_positive_negative_1(results):
    
    #nltk.download('stopwords')
    stopwords_set = set(stopwords.words("english"))
    polarity = []

    for index,i in results.iterrows():
        words_without_links = [word for word in i['tweet'].split() if (('https' not in word) and (
            '@' not in word) and ('http' not in word) and ((word in 'not') or (word not in stopwords_set)))]
        temp = ' '.join(words_without_links)
        temp = temp.strip()
        if(len(temp) > 100):

            blob = TextBlob(temp)
            polarity.append([temp, blob.sentiment.polarity,
                             blob.sentiment.subjectivity, len(temp)])

    df = pd.DataFrame(data=polarity, columns=[
                      'Tweet', 'Polarity', 'Subjectivity', 'Length'])
   # print(df.head())

    df_s = df.sort_values('Polarity')

    return df_s