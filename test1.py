# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:46:30 2019

@author: MUKHESH
"""
from spacy.lang.en import English
import spacy

nlp=spacy.load('en')
#nlp=English()
doc=nlp(u"Mukhesh is a good boy.")
for sen in doc:
    print(sen.pos_)