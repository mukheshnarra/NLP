# -*- coding: utf-8 -*-
"""
Created on Sun May 26 14:31:48 2019

@author: MUKHESH
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 19 15:08:03 2019

@author: MUKHESH
"""

import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
import random
from nltk.corpus import movie_reviews
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI
from statistics import mode
from sklearn.naive_bayes import MultinomialNB,BernoulliNB,GaussianNB
from sklearn.svm import SVC,NuSVC,LinearSVC
from sklearn.linear_model import LogisticRegression,SGDClassifier


# 

class Voteclassifier(ClassifierI):
    def __init__(self,*classifier):
        self._classifier=classifier
    def classify(self,features):
        vote=[]
        for c in self._classifier:
            v=c.classify(features)
            vote.append(v)
        #print(vote)
        return mode(vote)
    def confidence(self,features):
        vote=[]
        for c in self._classifier:
            v=c.classify(features)
            vote.append(v)
        conf=vote.count(mode(vote))
        return conf/len(vote)



with open('pickle/document.pickle','rb') as f:
    document=pickle.load(f)

with open('pickle/features.pickle','rb') as f:
    words=pickle.load(f)
#
def feature_extraction(documents):
    words_set=word_tokenize(documents)
    feature={}
    for w in words:
        feature[w]=(w in words_set)
    return feature

with open('nltk_naive.pickle','rb') as f:
    classifier=pickle.load(f)

with open('pickle/MB_classifier.pickle','rb') as f:
    MB_classifier=pickle.load(f)

with open('pickle/BE_classifier.pickle','rb') as f:
    BE_classifier=pickle.load(f)

with open('pickle/LogisticRegression_classifier.pickle','rb') as f:
    LogisticRegression_classifier=pickle.load(f)

with open('pickle/SGDClassifier_classifier.pickle','rb') as f:
    SGDClassifier_classifier=pickle.load(f)

#with open('pickle/SVC_classifierpickle','rb') as f:
#    SVC_classifier=pickle.load(f)

with open('pickle/LinearSVC_classifier.pickle','rb') as f:
    LinearSVC_classifier=pickle.load(f)

with open('pickle/NuSVC_classifier.pickle','rb') as f:
    NuSVC_classifier=pickle.load(f)

vote_classifier=Voteclassifier(MB_classifier,classifier,BE_classifier,LogisticRegression_classifier,SGDClassifier_classifier,LinearSVC_classifier,NuSVC_classifier)

def sentiment(text):
    facts=feature_extraction(text)
    
    return (vote_classifier.classify(facts),vote_classifier.confidence(facts)*100)
