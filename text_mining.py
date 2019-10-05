# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 22:54:13 2019

@author: MUKHESH
#"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import nltk
import textmining
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
import re
import textblob
import numpy as np


os.chdir('C:/Users/MUKHESH/OneDrive/Documents/Python Scripts/NLP/Exploring Text Data')
data=pd.read_csv('tweets.csv',encoding='ISO-8859-1',usecols=['text'],nrows=1000)
stop=set(nltk.corpus.stopwords.words('english'))
punctuation=set(string.punctuation)
#print(data.head(1))

def clean_text_http(data):
    data=re.sub(r'RT','',data)
    data=re.sub(r'&amp;','',data)
    data=re.sub(r'http(s?):\/\/t.co\/[a-zA-Z0-9]+','',data)
    data=re.sub(r'@[\w\d_]+:{1}','',data)
    data=re.sub(r'<[\w\d\s+:/.]+>','',data)
    return data

def clean_text(data):
    stop_free=' '.join([i for i in data.lower().split() if i not in stop])
    punc_free=''.join(c for c in stop_free if c not in  punctuation)
    num_free=''.join(c for c in punc_free if not c.isdigit())
    return num_free

data['text']=data.text.apply(clean_text_http)
data_clean=[clean_text(data.iloc[i,0]) for i in range(data.shape[0])]

tdm=textmining.TermDocumentMatrix()
for i in data_clean:
    tdm.add_doc(i)
tdm.write_csv(b'TDM_file.csv',cutoff=1)
tdm_data=pd.read_csv('TDM_file.csv')
print(tdm_data.shape)
data_clean=pd.DataFrame(data_clean)
data_clean.columns=['text']
#wordcloud=WordCloud(width=1000,height=1200,stopwords=STOPWORDS,background_color='white').generate(' '.join(data_clean['text']))
#plt.figure(figsize=(15,8))
#plt.imshow(wordcloud)
#plt.axis("off")
#plt.show()
#wordcloud.to_file('wordcloud.png')
final_list_results=pd.DataFrame()

def Sentiment_analysis():
    global final_list_results
    for i in range(data.shape[0]):
        blob=textblob.TextBlob(data.iloc[i,0])
        temp=pd.DataFrame({'Tweet':data.iloc[i,0],'Sentiment':blob.sentiment.polarity},index=[0])
        final_list_results=final_list_results.append(temp)


def Vader_sentiment_analysis():
    global final_list_results
    analyser=SentimentIntensityAnalyzer()
    for i in range(data.shape[0]):
        blob=analyser.polarity_scores(data.iloc[i,0])
        temp=pd.DataFrame({'Tweet':data.iloc[i,0],'Sentiment':blob['compound']},index=[0])
        final_list_results=final_list_results.append(temp)


inp=input('Enter value 1 or 2 if 1 selected it is textblob or 2 is selcted it is vadersentiment: ')



if (int(inp)==2):
    Vader_sentiment_analysis()
else:
    Sentiment_analysis()

final_list_results['Sentiment']=np.where(final_list_results.Sentiment>0,'pos',np.where(final_list_results.Sentiment<0,'neg','neu'))
print(final_list_results.head(5))
    
    
    
    

