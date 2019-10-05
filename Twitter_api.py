# -*- coding: utf-8 -*-
"""
Created on Tue May 28 00:34:49 2019

@author: MUKHESH
"""
import matplotlib.pyplot as plt
import tweepy
from tweepy import Stream,OAuthHandler,Cursor,API
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
import json 
#pd.options.display.max_columns=9
pd.options.display.max_colwidth=10000

class TwitterDatacapture():
    
    def clean_data(self,data):
        return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)",' ',data).split())
    def Twitter_sentiment(self,tweets):
        analysis=TextBlob(self.clean_data(tweets))
        if analysis.sentiment.polarity>0:
            return 'pos'
        elif analysis.sentiment.polarity==0:
            return 'neu'
        else:
            return 'neg'
    
    def Twitter_data(self,tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['text'])
        df['date']=np.array([tweet.created_at for tweet in tweets])
        df['likes']=np.array([tweet.favorite_count for tweet in tweets])
        df['retweet']=np.array([tweet.retweet_count for tweet in tweets])
        df['place']=np.array([tweet.place for tweet in tweets])
        df['source']=np.array([tweet.source for tweet in tweets])
        df['lang']=np.array([tweet.lang for tweet in tweets])
#        df=pd.DataFrame(data=[tweet.name for tweet in tweets],columns=['followers'])
        df['sentiment']=np.array([self.Twitter_sentiment(tweet) for tweet in df['text']])
        return df
        

class TwitterClient():
    
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuth().Authentication()
        self.client=API(self.auth)
        self.user=twitter_user
    
    def return_api(self):
        return self.client
    
    def get_user_time_twitts(self,num_twitts=1):
        twitts=[]
        for twitt in Cursor(self.client.user_timeline,id=self.user).items(num_twitts):
            twitts.append(twitt)
        return twitts
    
    def get_user_friends(self):
        friends=[]
        for friend in Cursor(self.client.friends,id=self.user).items():
            friends.append(friend)
        return friends
    def get_user_friends_id(self):
        friends=[]
        for friend in Cursor(self.client.friends_ids,id=self.user).items():
            friends.append(friend)
        return friends

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
            with open(self.file_name,'a',encoding='utf-8') as f:
                f.write(d['text'])
        except BaseException as e:
            print('The error status is:',str(e))
        return True
    def on_error(self,status):
        print(status)

if __name__=='__main__':
    hash_tag=['prabhas','sex','narendra modi','rahul gandhi','congress','BJP']
    streamer=TweetStreamer()
    streamer.streamer('tweet.json',hash_tag)
#    twitter_client=TwitterClient('mohitgupta')
#    
#    print(twitter_client.get_user_time_twitts(2))    
#    twitter_client=TwitterClient().return_api()
#    tweets=twitter_client.user_timeline(screen_name='narendramodi',count=200)
#    followers=twitter_client.followers(screen_name='mohit8302926301')
#    print(dir(followers[0]))
#    try:
#        status=twitter_client.send_direct_message(screen_name='NarraMukhesh', text='hi,hello')
#        print(status)                                    
#    except tweepy.error.TweepError:
#       print(tweepy.error.TweepError)

#    df=TwitterDatacapture().Twitter_data(tweets)  
#    print(df.head(10))
#    time_likes=pd.Series(data=df['likes'].values,index=df['date'])
#    time_likes.plot(figsize=(16,4),label='likes',legend=True)
#    time_retweet=pd.Series(data=df['retweet'].values,index=df['date'])
#    time_retweet.plot(figsize=(16,4),label='retweet',legend=True)
#    plt.show()