from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

# Create your views here.
def country_us(request):
    df = classifying_positive_negative('location:"United States"')
    return render(request, 'Country_wise_sentiment.html',{'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': "United States",'len':20})

def country_india(request):
    df = classifying_positive_negative('location:"India"')
    return render(request, 'Country_wise_sentiment.html',{'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': "India",'len':20})

def country_uk(request):
    df = classifying_positive_negative('location:"United Kingdom"')
    return render(request, 'Country_wise_sentiment.html',{'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': "United Kingdom",'len':20})
    
def country_can(request):
    df = classifying_positive_negative('location:"Canada"')
    return render(request, 'Country_wise_sentiment.html',{'data_top': df.head(n=10), 'data_bottom': df.tail(n=10), 'a': "Canada",'len':10})


def classifying_positive_negative(a):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)

    results = solr.search("*:*", rows=20000, fq = a)
    #nltk.download('stopwords')
    stopwords_set = set(stopwords.words("english"))
    polarity = []

    for i in results:
        words_without_links = [word for word in i['tweet'][0].split() if (('https' not in word) and (
            '@' not in word) and ('http' not in word) and ((word == 'not') or (word not in stopwords_set)))]
        temp = ' '.join(words_without_links)
        temp = temp.strip()
        if(len(temp) >10):

            blob = TextBlob(temp)
            polarity.append([i['tweet'][0], blob.sentiment.polarity,
                             blob.sentiment.subjectivity, len(temp)])

    df = pd.DataFrame(data=polarity, columns=[
                      'Tweet', 'Polarity', 'Subjectivity', 'Length'])
   # print(df.head())

    df_s = df.sort_values('Polarity')

    return df_s