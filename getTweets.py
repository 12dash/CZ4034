# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:01:17 2020

@author: 18moh
"""

import os
import tweepy as tw
import pandas as pd
import numpy as np
import solr

consumer_key='0OXA7QU4jqoInCMCyJZaneHsE'
consumer_secret='dDDGRta6UJ24k9CQG9v088VXawLgEX3czvY1EKriIIPgT1RW95'
access_token='1236865060544212993-72bAPQdeMpXoc6MPchsBAkvCzZRGDT'
access_token_secret='4bWJoY6yemqoG13Cb9bV6rX1nBrIqvt0I5gNxXwIqMuip'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def getTweets(keyword, number):
    collection=pd.DataFrame(columns=['keyword','id','tweet','date','location','retweets','likes'])
    
    try:
        tweets = tw.Cursor(api.search,
                           q=keyword,
                           lang="en").items(number)
    except:
        return collection
    
    for x in tweets:
        if(x.is_quote_status==False and x.retweeted==False):
            print(x.created_at)
            row={'keyword':keyword, 
                 'id':x._json['id'], 
                 'tweet':x._json['text'], 
                 'date':x._json['created_at'], 
                 'location':x._json['place'], 
                 'retweets':x._json['retweet_count'], 
                 'likes':x._json['favorite_count']}
            collection=collection.append(row, ignore_index=True)
            
    print(collection)
    return collection

def searchUpdate(query, number):
    s=solr.SolrConnection('http://localhost:8083/solr')
    
    col=getTweets(query, number)
    
    for i in range(len(col)):
        doc={'keyword':col.at[i,'keyword'],
             'id':col.at[i,'id'],
             'tweet':col.at[i,'tweet'],
             'date':col.at[i,'date'],
             'location':col.at[i,'location'],
             'retweets':col.at[i,'retweets'],
             'likes':col.at[i,'likes']}
        s.add(doc, commit=True)
    
    
    
    









