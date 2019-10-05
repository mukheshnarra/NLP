# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:07:49 2019

@author: MUKHESH
"""

#from nltk.tokenize import sent_tokenize,word_tokenize
#from nltk.corpus   import stopwords
#from nltk.stem import PorterStemmer
#example='hello how are you? i am fine, well iam taking leave for this weekend can you please take the work what iam working. That''s Ok .Thank you '
#sent=sent_tokenize(example)
#word=word_tokenize(example)
#stop=set(stopwords.words('english'))
#stem=PorterStemmer()
#for i,words in enumerate(sent):
#    print(i,words)
#print(stop)
#filtered_words=[words for words in word_tokenize(example) if words not in stop]
#print(filtered_words)
#for words in word_tokenize(example):
#    print(stem.stem(words))
#'''
#NNP=PROPER NOUN
#NN=NOUN,SINGULAR
# POS=POSSESSIVE ENDING
#'''
import nltk
from nltk.corpus import state_union,gutenberg,wordnet
from nltk.tokenize import PunktSentenceTokenizer,sent_tokenize
from  nltk.stem import WordNetLemmatizer

syn=wordnet.synsets('good')
for s in syn:
    print(s.definition())
    print(s.examples())
synonyms=[]
antonyms=[]
for s in syn:
    for l in s.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(synonyms)
print(antonyms)
#w1=wordnet.synset('boat.n.01')
#w2=wordnet.synset('car.n.01')
#print(w1.wup_similarity(w2))
#lemmatizer=WordNetLemmatizer()
#print(lemmatizer.lemmatize('better',pos='a'))
#sample=gutenberg.raw("bible-kjv.txt")
#text=sent_tokenize(sample)
#print(text[5:12])

#sample_text=state_union.raw('2005-GWBush.txt')
#train_text=state_union.raw('2006-GWBush.txt')
#custom_tokenizer=PunktSentenceTokenizer(train_text)
#sentence=custom_tokenizer.tokenize(sample_text)
##print(sentence)
#try:
#    for i in sentence:
#        words=nltk.word_tokenize(i)
#        tag=nltk.pos_tag(words)
#        print(tag)
#        #chunk=r'''Chunk:{<RR.?>*<VB.?>*<NN.?>}'''
##        chunk=r'''Chunk:{<.*>+}
##                   }<VB.|IN|DT>{'''
##        chunk_parser=nltk.RegexpParser(chunk)
##        chunkked=chunk_parser.parse(tag)
##        chunkked=nltk.ne_chunk(tag,binary=True)
##        print(chunkked)
##        chunkked.draw()
#        
#except Exception as e:
#    print(e)