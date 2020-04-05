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


def Ssearch(request):
    print(request.GET)
    return render(request, 'static_sentiment.html')


def Ssearch_output(request):
    query = request.GET['search']
    a = query
    query = request.GET['search']   
    query = 'tweet:'+ "\""+ query +"\""   

    data = solr_search(query)

    data = classifying_positive_negative_1(data)
    
    return render(request, 'static_sentiment_result.html', {'data_top': data.head(n=10), 'data_bottom': data.tail(n=10),'a': a})

def solr_search(a):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)     
    results = solr.search(a,rows = 500, f1 = "*,score", sort="likes desc")
    print(results)
    return results

def classifying_positive_negative_1(results):
    
    #nltk.download('stopwords')
    stopwords_set = set(stopwords.words("english"))
    polarity = []

    for i in results:
        words_without_links = [word for word in i['tweet'][0].split() if (('https' not in word) and (
            '@' not in word) and ('http' not in word) and ((word in 'not') or (word not in stopwords_set)))]
        temp = ' '.join(words_without_links)
        temp = temp.strip()
        if(len(temp) > 10):

            blob = TextBlob(temp)
            polarity.append([i['tweet'][0], blob.sentiment.polarity,
                             blob.sentiment.subjectivity, len(temp)])

    df = pd.DataFrame(data=polarity, columns=[
                      'Tweet', 'Polarity', 'Subjectivity', 'Length'])
   # print(df.head())

    df_s = df.sort_values('Polarity')

    return df_s