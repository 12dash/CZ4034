import json
import pandas as pd
from textblob import TextBlob

data_list= []
with open('key_corona.json',"r", encoding="utf-8") as json_file:
    data_list = json.load(json_file)

tweet_data_frame = pd.DataFrame.from_dict(data_list)
polarity = []
i = 0

for index,row in tweet_data_frame.iterrows():
    blob = TextBlob(row['tweet'])
    polarity.append([row['tweet'],blob.sentiment])
    i += 1
    if( i > 1000):
        break

for i in polarity:
    if(i[1].polarity<-0.7):
        print(i[0]+'\t'+ str(i[1].polarity))
