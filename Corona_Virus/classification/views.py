from django.shortcuts import render

from django.views.generic import TemplateView
from django.shortcuts import render

import pandas as pd
import numpy as np
import math

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn


#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics import accuracy_score
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier
from dummy import dummy_fun
import pickle
from joblib import load, dump

import pysolr
# Create your views here.
#from sklearn.ensemble import BaggingClassifier
#from sklearn import svm
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import confusion_matrix

def classification(request):
    #svbag,forest,tfidf = data_preprocess()
    #t = classifyRecord('One country addressing the COVID 19 crisis with competence. BBC News - Coronavirus in South Korea: How \'trace, test and treat\' may be saving lives https://t.co/3Y3blkbsqJ', svbag, forest, tfidf)
    #print(t)
    #return render(request,"classification.html")
    svbag = load('model_svbag.joblib')
    print('loaded svbag')
    forest = load('model_forest.joblib')
    print('loaded forest')  
    tfidf = load('model_tfidf.joblib')
    print('loaded forest')   
    data = solr()
    l = get_tweets_results(data,svbag,forest,tfidf)
    print([classifyRecord('One country addressing the COVID 19 crisis with competence. BBC News - Coronavirus in South Korea: How \'trace, test and treat\' may be saving lives https://t.co/3Y3blkbsqJ', svbag, forest, tfidf)])
    return render(request,"classification_results.html",{'data': l })


def solr():
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)     
    results = solr.search("*:*", rows=100) 
    return results

def get_tweets_results(data,svbag,forest,tfidf):
    l = []
    for i in data:
       temp =  get_type(classifyRecord(i['tweet'][0],svbag, forest, tfidf))
       l.append([i['tweet'][0], temp]  )  
    return l

def stop():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english')) 

    stop_words.add('.')
    stop_words.add(';')
    stop_words.add(':')
    stop_words.add('...')
    stop_words.add('=')
    stop_words.add('')
    stop_words.add(' ')
    stop_words.add(',')
    stop_words.add('>')
    stop_words.add('-')
    stop_words.add('/')
    stop_words.add('//')
    stop_words.add('-')
    stop_words.add('(')
    stop_words.add(')')
    stop_words.add('\'')
    stop_words.add('\"')
    return stop_words

def get_type(s):
    if(s==0):
        return "Miscellaneous (Sorry we can not categorize this)"
    if(s==1):
        return "News and Facts"
    if(s==2):        
        return "Speculation (I am getting bored so ...)"
    if(s==3):
        return "Reaction or Opinion (Its my opinion)"


#Classifier, returns the class of the string tweet
def classifyRecord(tweet, svbag, forest, tfidf):
    row={'tweet':[tweet]}
    temp=pd.DataFrame(row,columns=['tweet'])
    
    temp['tweet*']=''
    if(type(temp.at[0,'tweet'])!=float):
        temp.at[0,'tweet*']=temp.at[0,'tweet']
    temp.at[0,'tweet*']=temp.at[0,'tweet*'].lower()
    temp.at[0,'tweet*']=word_tokenize(temp.at[0,'tweet*'])
    temp['prelength']=0
    temp.at[0,'prelength']=len(temp.at[0,'tweet*'])
    stop_words = stop()
    pos=['NN', 'NNS', 'PRP', 'VBP', "''",
       'TO', 'VB', 'IN', 'VBG', '.', 'JJ', 'DT', ',', 'VBZ', 'RP', 'MD', 'RB',
       'WP', '``', 'RBR', 'CC', 'VBN', ':', 'CD', 'VBD', 'WDT', 'PRP$',
       'WRB', 'NNP', 'JJR', 'FW', 'PDT', 'EX', '$', 'POS', '(', ')', '#',
       'JJS', 'RBS', 'SYM', 'NNPS', 'LS', 'UH', 'WP$']
    for x in pos:
        temp[x]=0
    
    s=temp.at[0,'tweet*']
    tagged=nltk.pos_tag(s) 
    for x in tagged:
        temp.at[0,x[1]]+=1
    
    l=[]
    for x in temp.at[0,'tweet*']:
        if(x not in stop_words):
            l.append(x)
    temp.at[0,'tweet*']=l
    
    ps=PorterStemmer()
    l=[]
    for x in temp.at[0,'tweet*']:
        y=ps.stem(x)
        if(y not in stop_words):
            l.append(y)
    temp.at[0,'tweet*']=l
    
    temp['postlength']=0
    temp.at[0,'postlength']=len(temp.at[0,'tweet*'])
    temp['removed']=temp['prelength']-temp['postlength']
    temp['removeratio']=1.0
    if(temp.at[0,'prelength']!=0):
        temp.at[0,'removeratio']=temp.at[0,'removed']/temp.at[0,'prelength']
        
    temp['prob0']=0.0
    temp['prob1']=0.0
    temp['prob2']=0.0
    temp['prob3']=0.0

    temptfidf=tfidf.transform(temp['tweet*'])
    pred1=svbag.predict_proba(temptfidf)        
    pred=forest.predict(temp[['prelength', 'NN', 'NNS', 'PRP', 'VBP',
       'TO', 'VB', 'IN', 'VBG', '.', 'JJ', 'DT', ',', 'VBZ', 'RP', 'MD', 'RB',
       'WP', '``', 'RBR', 'CC', 'VBN', ':', 'CD', 'VBD', 'WDT', 'PRP$',
       'WRB', 'NNP', 'JJR', 'FW', 'PDT', 'EX', '$', 'POS', '(', ')', '#',
       'JJS', 'RBS', 'SYM', 'NNPS', 'LS', 'UH', 'WP$', 'postlength', 'removed',
       'removeratio', 'prob0', 'prob1', 'prob2', 'prob3']])        
    return pred[0]