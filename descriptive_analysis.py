# -*- coding: utf-8 -*-
"""
Created on Sat May 30 19:40:15 2015

@author: Carlo
"""
from collections import defaultdict
import string
from nltk.corpus import stopwords
from gensim import corpora, models, similarities


locations = defaultdict(int)
for b in businesses:
    locations[b['city']] += 1
    
popularLocations = []
for l in locations:
    popularLocations.append([locations[l], l])
    
popularLocations.sort()
popularLocations.reverse()

#analize review corpus
punctuation = set(string.punctuation)

rCorpus = []
for r in reviews:
    ### Ignore capitalization and remove punctuation
    rCorpus.append(''.join([c for c in r['text'].lower() if not c in punctuation]))
    
#remove stopwords
stops = set(stopwords.words('english'))    
rCorpus = [[word for word in review.split() if word not in stops] for review in rCorpus]

# remove words that appear only once
word_freq = defaultdict(int)

for r in rCorpus:
    for word in r:
        word_freq[word] += 1
        
rCorpus = [[word for word in review if word_freq[word] > 1] for review in rCorpus]

dictionary = corpora.Dictionary(rCorpus)
#store dictionary
dictionary.save('/Users/Carlo/Documents/Yelp_LDA/dict_v1.dict')

#gensim
corpus = [dictionary.doc2bow(review) for review in rCorpus]
corpora.MmCorpus.serialize('corpus_v1.mm', corpus)

#load dictionary and corpus
dictionary = corpora.Dictionary.load('dict_v1.dict')
corpus = corpora.MmCorpus('corpus_v1.mm')

