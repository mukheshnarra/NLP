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


#document=[(list(movie_reviews.words(fileId)),category)
#            for category in movie_reviews.categories()
#            for fileId in movie_reviews.fileids(category)]
#random.shuffle(document)
#print(document[1])
document=[]
all_words=[]
positive=open('positive_review.txt','r').read()
negative=open('negative_review.txt','r').read()
allowed_word_types = ["J"]

for i in positive.split('\n'):
    words = word_tokenize(i)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
    document.append((i,'pos'))
for i in negative.split('\n'):
    words=[]
    words = word_tokenize(i)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
    document.append((i,'neg'))
with open('pickle/document.pickle','wb') as f:
    pickle.dump(document,f)
    
#all_words=[]
#for words in word_tokenize(positive):
#    all_words.append(words.lower())
#for words in word_tokenize(negative):
#    all_words.append(words.lower())
#    
#for words in movie_reviews.words():
#    all_words.append(words)
#    
all_words=nltk.FreqDist(all_words)
##print(all_words.most_common(14))
##print(len(all_words))
words=list(all_words.keys())[:5000]
with open('pickle/features.pickle','wb') as f:
    pickle.dump(words,f)
#
def feature_extraction(documents):
    words_set=word_tokenize(documents)
    feature={}
    for w in words:
        feature[w]=(w in words_set)
    return feature
        
#print(feature_extraction(movie_reviews.words('neg/cv000_29416.txt')))
feature_set=[(feature_extraction(rev),category) for rev,category in document]
random.shuffle(feature_set)
train_set=feature_set[:10000]
test_set=feature_set[10000:]
classifier=nltk.NaiveBayesClassifier.train(train_set)
#with open('nltk_naive.pickle','rb') as f:
#    classifier=pickle.load(f)
print('nltk naive accuracy: ',nltk.classify.accuracy(classifier,test_set)*100)
print(classifier.show_most_informative_features(15))
with open('pickle/nltk_naive_bayes.pickle','wb') as f:
    pickle.dump(classifier,f)
MB_classifier=SklearnClassifier(MultinomialNB())
MB_classifier.train(train_set)
print('MB_classifier accuracy: ',nltk.classify.accuracy(MB_classifier,test_set)*100)
with open('pickle/MB_classifier.pickle','wb') as f:
    pickle.dump(MB_classifier,f)
BE_classifier=SklearnClassifier(BernoulliNB())
BE_classifier.train(train_set)
print('BE_classifier accuracy: ',nltk.classify.accuracy(BE_classifier,test_set)*100)
with open('pickle/BE_classifier.pickle','wb') as f:
    pickle.dump(BE_classifier,f)
LogisticRegression_classifier=SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(train_set)
print('LogisticRegression_classifier accuracy: ',nltk.classify.accuracy(LogisticRegression_classifier,test_set)*100)
with open('pickle/LogisticRegression_classifier.pickle','wb') as f:
    pickle.dump(LogisticRegression_classifier,f)
SGDClassifier_classifier=SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(train_set)
print('SGDClassifier_classifier accuracy: ',nltk.classify.accuracy(SGDClassifier_classifier,test_set)*100)
with open('pickle/SGDClassifier_classifier.pickle','wb') as f:
    pickle.dump(SGDClassifier_classifier,f)
SVC_classifier=SklearnClassifier(SVC())
SVC_classifier.train(train_set)
print('SVC_classifier accuracy: ',nltk.classify.accuracy(SVC_classifier,test_set)*100)
with open('pickle/SVC_classifier.pickle','wb') as f:
    pickle.dump(SVC_classifier,f)
LinearSVC_classifier=SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(train_set)
print('LinearSVC_classifier accuracy: ',nltk.classify.accuracy(LinearSVC_classifier,test_set)*100)
with open('pickle/LinearSVC_classifier.pickle','wb') as f:
    pickle.dump(LinearSVC_classifier,f)
NuSVC_classifier=SklearnClassifier(NuSVC())
NuSVC_classifier.train(train_set)
print('NuSVC_classifier accuracy: ',nltk.classify.accuracy(NuSVC_classifier,test_set)*100)
with open('pickle/NuSVC_classifier.pickle','wb') as f:
    pickle.dump(NuSVC_classifier,f)
vote_classifier=Voteclassifier(MB_classifier,classifier,BE_classifier,LogisticRegression_classifier,SGDClassifier_classifier,LinearSVC_classifier,NuSVC_classifier)
print('vote_classifier accuracy: ',nltk.classify.accuracy(vote_classifier,test_set)*100)