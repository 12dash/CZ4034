from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

def classifying_positive_negative_1():
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)

    results = solr.search("*:*", rows=10000)
    #nltk.download('stopwords')
    stopwords_set = set(stopwords.words("english"))
    polarity = []

    for i in results:
        words_without_links = [word for word in i['tweet'][0].split() if (('https' not in word) and (
            '@' not in word) and ('http' not in word) and ((word == 'not') or (word not in stopwords_set)))]
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

def tweet_sentic(request):
    df = classifying_positive_negative_1()
    print(df.head())
    return render(request, 'tweet_senti.html', {'data_top': df.head(n=100), 'data_bottom': df.tail(n=100)})
    