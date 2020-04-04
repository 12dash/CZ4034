from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import pandas as pd
from textblob import TextBlob

def finding_posistive_tweets(request):
    a = "corona"
    df = classifying_positive_negative(a)
    return render(request, 'sentiment.html',{'data_top':df.head(n=20),'data_bottom':df.tail(n=20),'a':a})

def classifying_positive_negative(a):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)
    a ='keyword:'+ "\""+ a +"\""
    results = solr.search(a,rows = 20000)

    polarity = []

    for i in results:
        blob = TextBlob(i['tweet'][0])
        polarity.append([i['tweet'],blob.sentiment.polarity])   

    df = pd.DataFrame(data = polarity,columns = ['Tweet','Sentiment'])   
    print(df.head())

    df_s = df.sort_values('Sentiment')

    return df_s