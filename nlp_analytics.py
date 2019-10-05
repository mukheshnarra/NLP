# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:01:10 2019

@author: MUKHESH
"""
import zipfile
import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import re

zipf=zipfile.ZipFile('C:/Users/MUKHESH/Downloads/Exploring_Text_Data.zip',mode='r')
os.chdir('C:/Users/MUKHESH/OneDrive/Documents/Python Scripts/NLP')

if(os.path.isdir('C:/Users/MUKHESH/OneDrive/Documents/Python Scripts/NLP/Exploring Text Data')==0):
    zipf.extractall('C:/Users/MUKHESH/OneDrive/Documents/Python Scripts/NLP')
    zipf.close()
    
os.chdir('./Exploring Text Data')


def genfreq(text):
    word_list=[]
    for tweet in text.split():
        word_list.extend(tweet)
    
    FreqDist=pd.Series(word_list).value_counts()
    return FreqDist

def cleantext(text):
    text=re.sub(r'RT','',text)
    text=re.sub(r'&amp;','',text)
    text=re.sub(r'[?,-;:#@.+%]','',text)
    text=text.lower()
    return text


data=pd.read_csv('tweets.csv',encoding='ISO-8859-1')
data.drop(columns=['Unnamed: 0'],inplace=True)
data['text']=data.text.apply(lambda x:cleantext(x))
word_list=genfreq(data.text.str)
word_list=word_list.drop(labels=STOPWORDS,errors='ignore')
wc=WordCloud(height=400,width=330,background_color='white',max_words=100).generate_from_frequencies(word_list)
plt.figure(figsize=(12,8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
