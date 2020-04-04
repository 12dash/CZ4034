from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords


def tweet_option(request):
    return render(request, 'Analysis_option.html')


def corona(request):
    a = "corona"
    df = classifying_positive_negative(a)
    a2 = "covid"
    df1 = classifying_positive_negative(a2)
    df = pd.concat([df, df1])
    print(df.head())
    return render(request, 'sentiment.html', {'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': "Corona"})


def epidemic(request):
    a1 = "epidemic"
    df = classifying_positive_negative(a1)
    a2 = "pandemic"
    df1 = classifying_positive_negative(a2)
    df = pd.concat([df, df1])
    return render(request, 'sentiment.html', {'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': "Epidemic"})


def safe(request):
    a = "safe"
    df = classifying_positive_negative(a)
    return render(request, 'sentiment.html', {'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': a})


def contagious(request):
    a = "contagious"
    df = classifying_positive_negative(a)
    return render(request, 'sentiment.html', {'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': a})


def quarantine(request):
    a = "quarantine"
    df = classifying_positive_negative(a)
    return render(request, 'sentiment.html', {'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': a})


def china(request):
    a = "china"
    df = classifying_positive_negative(a)
    return render(request, 'sentiment.html', {'data_top': df.head(n=20), 'data_bottom': df.tail(n=20), 'a': a})


def classifying_positive_negative(a):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)
    q = a
    a = 'keyword:' + "\"" + a + "\""
    results = solr.search(a, rows=20000)
    nltk.download('stopwords')
    stopwords_set = set(stopwords.words("english"))
    polarity = []

    for i in results:
        words_without_links = [word for word in i['tweet'][0].split() if (('https' not in word) and (
            '@' not in word) and ('http' not in word) and ((word == 'not') or (word not in stopwords_set)))]
        temp = ' '.join(words_without_links)
        temp = temp.strip()
        if(len(temp) > 100):

            blob = TextBlob(temp)
            polarity.append([i['tweet'][0], blob.sentiment.polarity,
                             blob.sentiment.subjectivity, len(temp)])

    df = pd.DataFrame(data=polarity, columns=[
                      'Tweet', 'Polarity', 'Subjectivity', 'Length'])
   # print(df.head())

    df_s = df.sort_values('Polarity')

    return df_s
