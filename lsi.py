# -*- coding: utf-8 -*-
"""
Created on Tue Jun 02 04:09:20 2015

@author: Carlo
"""

from collections import defaultdict
import string
from nltk.corpus import stopwords
from gensim import corpora, models, similarities

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

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
topics = lsi.print_topics(50)

for i in range(len(topics)):
    print "topic #%r: " %(i+1), topics[i]
    
lsi.save('model.lsi')