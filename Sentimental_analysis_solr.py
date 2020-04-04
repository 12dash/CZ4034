from __future__ import print_function
import pysolr
import pandas as pd
from textblob import TextBlob

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)
results = solr.search('tweet:corona',rows = 20000)

polarity = []

for i in results:
    blob = TextBlob(i['tweet'][0])
    polarity.append([i['tweet'],blob.sentiment.polarity])   

df = pd.DataFrame(data = polarity,columns = ['Tweet','Sentiment'])   
print(df.head())

df_s = df.sort_values('Sentiment')

print(df_s.head())
print(df_s.tail())