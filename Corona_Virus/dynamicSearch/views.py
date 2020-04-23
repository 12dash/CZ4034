from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import os
import tweepy as tw
import pandas as pd
import numpy as np
import pysolr

# Create your views here.


def Dsearch(request):
    print(request.GET)
    return render(request, 'Dynamic_search.html')


def Dsearch_output(request):
    query = request.GET['search']
    query = "\"" + query + "\""
    print(query)
    data = get_tweets(query)
    data = data.sort_values(['retweets'], ascending=False)
    print(data)
    return render(request, 'Dynamic_results.html', {'data': data})

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
    number = 10

    try:
        tweets = tw.Cursor(api.search,
                           q=keyword,
                           lang="en").items(number)
    except:
        return collection

    for x in tweets:
        if(x.is_quote_status == False and x.retweeted == False):
            print(x.created_at)
            row = {'keyword': keyword,
                   'id': x._json['id'],
                   'tweet': x._json['text'],
                   'date': x._json['created_at'],
                   'location': x._json['place'],
                   'retweets': x._json['retweet_count'],
                   'likes': x._json['favorite_count']}
            collection = collection.append(row, ignore_index=True)

    return collection
