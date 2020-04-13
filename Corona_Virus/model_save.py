import pandas as pd
import numpy as np
import math

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from dummy import dummy_fun
dataset=pd.read_csv('https://raw.githubusercontent.com/mohitprashant/COVID-19-Tweet-Classification/master/100fromeach.csv')

dataset.head()
df = dataset
df = df.dropna(subset=['tweet'])

#Create a copy of the tweet column

dataset['tweet*']=''

for i in range(len(dataset)):
    if(type(dataset.at[i,'tweet'])!=float):
        dataset.at[i,'tweet*']=dataset.at[i,'tweet']    

#Lowercase all tweets

for i in range(len(dataset)):
    dataset.at[i,'tweet*']=dataset.at[i,'tweet*'].lower()

#Tokenize

for i in range(len(dataset)):
    dataset.at[i,'tweet*']=word_tokenize(dataset.at[i,'tweet*'])

#Tweet length

dataset['prelength']=0

for i in range(len(dataset)):
    dataset.at[i,'prelength']=len(dataset.at[i,'tweet*'])


#Parts of speech tag count

nltk.download('tagsets')
nltk.download('averaged_perceptron_tagger')
  
l=[]

for i in range(len(dataset)):
    s=dataset.at[i,'tweet*']
    tagged=nltk.pos_tag(s) 
    for x in tagged:
        if(x[1] not in l):
            l.append(x[1])
            
for x in l:
    dataset[x]=0

for i in range(len(dataset)):
    s=dataset.at[i,'tweet*']
    tagged=nltk.pos_tag(s) 
    for x in tagged:
        dataset.at[i,x[1]]+=1
            
#Adapted from https://www.geeksforgeeks.org/part-speech-tagging-stop-words-using-nltk-python/

#Remove stop words

nltk.download('stopwords')
stop_words = set(stopwords.words('english')) 
nltk.download('punkt')
nltk.download('wordnet')

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

def noNumbers(s):
    numbers=['0','1','2','3','4','5','6','7','8','9']
    for x in numbers:
        if(x in s):
            return False
    return True

for i in range(len(dataset)):
    l=[]
    for x in dataset.at[i,'tweet*']:
        if(x not in stop_words):
            l.append(x)
    dataset.at[i,'tweet*']=l

#Stem words

ps=PorterStemmer()

for i in range(len(dataset)):
    l=[]
    for x in dataset.at[i,'tweet*']:
        y=ps.stem(x)
        if(y not in stop_words):
            l.append(y)
    dataset.at[i,'tweet*']=l

#Tweet length after processing

dataset['postlength']=0

for i in range(len(dataset)):
    dataset.at[i,'postlength']=len(dataset.at[i,'tweet*'])
    
dataset['removed']=dataset['prelength']-dataset['postlength']

dataset['removeratio']=1.0

for i in range(len(dataset)):
    if(dataset.at[i,'prelength']!=0):
        dataset.at[i,'removeratio']=dataset.at[i,'removed']/dataset.at[i,'prelength']

X_train, X_test, y_train, y_test=train_test_split(dataset['tweet*'], dataset['category'], test_size=0.1)

while(len(y_test.unique())!=4 or len(y_train.unique())!=4):
    X_train, X_test, y_train, y_test = train_test_split(dataset['tweet*'], dataset['category'], test_size = 0.1)



tfidf = TfidfVectorizer(
    analyzer='word',
    tokenizer=dummy_fun,
    preprocessor=dummy_fun,
    token_pattern=None)  

#Source - http://www.davidsbatista.net/blog/2018/02/28/TfidfVectorizer/

tfidf.fit(dataset['tweet*'])
X_train_tfidf=tfidf.transform(X_train)
X_test_tfidf=tfidf.transform(X_test)

from sklearn import svm

sv=svm.SVC(C=2.5, kernel='linear', degree=3, gamma='auto')

sv.fit(X_train_tfidf, y_train)

predict_sv=sv.predict(X_test_tfidf)

print("SVM Accuracy Score : ", accuracy_score(predict_sv, y_test)*100)

from sklearn.ensemble import BaggingClassifier

sv2=svm.SVC(C=2.5, kernel='linear', degree=3, gamma='auto')

svbag=BaggingClassifier(base_estimator=sv2, random_state=10, n_estimators=10, max_samples=1.0, max_features=1.0)

svbag.fit(X_train_tfidf, y_train)

predict_svbag=svbag.predict(X_test_tfidf)

print("SVM Accuracy Score : ", accuracy_score(predict_svbag, y_test)*100)

dataset['prob0']=0.0
dataset['prob1']=0.0
dataset['prob2']=0.0
dataset['prob3']=0.0

tweet_tfidf=tfidf.transform(dataset['tweet*'])

predicting=svbag.predict_proba(tweet_tfidf)

for i in range(len(dataset)):
    dataset.at[i,'prob0']=predicting[i][0]
    dataset.at[i,'prob1']=predicting[i][1]
    dataset.at[i,'prob2']=predicting[i][2]
    dataset.at[i,'prob3']=predicting[i][3]
    
X_train, X_test, y_train, y_test=train_test_split(dataset[['prelength', 'NN', 'NNS', 'PRP', 'VBP',
       'TO', 'VB', 'IN', 'VBG', '.', 'JJ', 'DT', ',', 'VBZ', 'RP', 'MD', 'RB',
       'WP', '``', 'RBR', 'CC', 'VBN', ':', 'CD', 'VBD', 'WDT', 'PRP$',
       'WRB', 'NNP', 'JJR', 'FW', 'PDT', 'EX', '$', 'POS', '(', ')', '#',
       'JJS', 'RBS', 'SYM', 'NNPS', 'LS', 'UH', 'WP$', 'postlength', 'removed',
       'removeratio', 'prob0', 'prob1', 'prob2', 'prob3']], dataset['category'], test_size=0.25)
from sklearn.ensemble import RandomForestClassifier

forest=RandomForestClassifier(n_estimators=100, max_depth=55, bootstrap=True, random_state=42)

forest.fit(X_train, y_train)

predict_forest=forest.predict(X_test)

from sklearn.metrics import confusion_matrix

conf=confusion_matrix(y_test, predict_forest)

accuracy=np.sum(np.diag(conf))/np.sum(conf)
recall=np.mean(np.diag(conf)/np.sum(conf, axis=1))
precision=np.mean(np.diag(conf)/np.sum(conf, axis=0))

print("Ensemble Accuracy Score : ", accuracy*100)
print("Ensemble Recall Score : ", recall*100)
print("Ensemble Precision Score : ", precision*100)
print("Ensemble F-Measure Score : ", (100*2*precision*recall)/(precision+recall))

from joblib import dump,load

dump(svbag,"model_svbag.joblib",compress=True)
dump(forest,"model_forest.joblib",compress=True)
dump(tfidf,"model_tfidf.joblib",compress=True)