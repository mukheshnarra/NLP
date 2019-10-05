# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 00:55:53 2019

@author: MUKHESH
"""

from kafka import KafkaProducer
from kafka.cluster import ClusterMetadata as cm
import kafka
from pymongo import MongoClient
from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
import json


class KafkaProducerClient():
    
    def producer(self,topic):
        producer=KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        consumer = kafka.KafkaConsumer( bootstrap_servers='localhost:9092')
        if topic not in consumer.topics():
            admin=kafka.admin.KafkaAdminClient(bootstrap_servers='localhost:9092')
            add_topic=[]
            add_topic.append(kafka.admin.NewTopic(name=topic,replication_factor=1,num_partitions=1))
            admin.create_topics(new_topics=add_topic)
        return producer,topic

class TwitterAuthkeys():
    def Auth(self):
        client=MongoClient()
        db=client['mydatabase']
        keys=db.keys
        token=list(keys.find())
        auth=OAuthHandler(token[0]['consumer_key'],token[0]['consumer_secret_key'])
        auth.set_access_token(token[0]['access_api_key'],token[0]['access_api_secret_key'])
        return auth

class StreamingListener(StreamListener):
    def __init__(self,producer,topic):
        self.producer=producer
        self.topic=topic
    
    def on_data(self,data):
        try:
            d=json.loads(data)
            self.producer.send(self.topic,d)
            
        except BaseException as e:
            print('The error status is :'+str(e))
        return True
    
    def on_error(self,status):
        print(status)
    


class TwitterStreamer():
    def __init__(self):
        self.auth=TwitterAuthkeys().Auth()
    def streaming(self,producer,topic,hashtag):
        listener=StreamingListener(producer,topic)
        stream=Stream(self.auth,listener)
        stream.filter(track=hash_tag,languages=['en'])        


if __name__=='__main__':
    hash_tag=['prabhas','sex','narendra modi','rahul gandhi','congress','BJP']
    producer,topic=KafkaProducerClient().producer('Twitter_live_twitts')
    streamer=TwitterStreamer()
    streamer.streaming(producer,topic,hash_tag)
    