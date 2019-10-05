# -*- coding: utf-8 -*-
"""
Created on Thu May 30 23:36:20 2019

@author: MUKHESH
"""
from tweepy import Stream,OAuthHandler,Cursor,API
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
import json 
import sentiment as s


class TwitterAuth():
     def Authentication(self):
         client=MongoClient()
         db=client['mydatabase']
         key=db.keys
         keys=list(key.find())
         auth=OAuthHandler(keys[0]['consumer_key'],keys[0]['consumer_secret_key'])
         auth.set_access_token(keys[0]['access_api_key'],keys[0]['access_api_secret_key'])
         return auth


class TweetStreamer():
    
    def __init__(self):
        self.auth=TwitterAuth().Authentication()
    
    def streamer(self,file_name,hash_tag):
        listener=Stout_listener(file_name)
        stream=Stream(self.auth,listener)
        stream.filter(track=hash_tag)


class Stout_listener(StreamListener):
    
    def __init__(self,filename):
        self.file_name=filename
    
    def on_data(self,data):
        #print(data)
        try:
            d=json.loads(data)
            category,confidence=s.sentiment(d['text'])
            if confidence >= 80:
                with open(self.file_name,'a',encoding='utf-8') as f:
                   f.write(category)
                   f.write('\n')
        except BaseException as e:
            print('The error status is:',str(e))
        return True
    def on_error(self,status):
        print(status)
        

if __name__=='__main__':
    hash_tag=['prabhas','sex','narendra modi','rahul gandhi','congress','BJP','BCCI']
    streamer=TweetStreamer()
    streamer.streamer('tweet.txt',hash_tag)
