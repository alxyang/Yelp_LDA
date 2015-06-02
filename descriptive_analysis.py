# -*- coding: utf-8 -*-
"""
Created on Sat May 30 19:40:15 2015

@author: Carlo
"""
from collections import defaultdict
import string
import numpy
import matplotlib.pyplot as plt


review_count = defaultdict(int)
for r in reviews:
    review_count[r['business_id']] += 1

popularBusinesses = []
for c in review_count:
    popularBusinesses.append([review_count[c], c])
    
popularBusinesses.sort()
popularBusinesses.reverse()

count = 1
while (1):
    if count > 1.0*len(popularBusinesses)/2:
        print popularBusinesses[count-1][0]
        break
    count +=1
    
x_to_y = defaultdict(int)
for c in popularBusinesses:
    x_to_y[c[0]] += 1
    

X = []
Y = []
for x in x_to_y:
    X.append(x)
    Y.append(x_to_y[x])
    
plt.plot(X, Y)
plt.title("Number of reviews per business")
plt.xlabel("Number of reviews")
plt.ylabel("Frequency of occurrence")

food_related = []
for b in businesses:
    for c in b['categories']:
        if c == 'Food' or c == 'Restaurants':
            food_related.append(b)
            break
        
    
    
for i in range(50):
    business_id = popularBusinesses[i][1]
    print "category:%s" %category[business_id], "count:%r" % popularBusinesses[i][0] 



#average number of words per review
rev_count = []
for r in reviews:
    rev_count.append(len(r['text'].split()))
rev_count.sort()
rev_count.reverse()

numpy.median(numpy.array(rev_count))

x_to_y = defaultdict(int)
for c in rev_count:
    x_to_y[c] += 1
    

X = []
Y = []
for x in x_to_y:
    X.append(x)
    Y.append(x_to_y[x])
    
plt.plot(X, Y)
plt.title("Number of words per review")
plt.xlabel("Number of words")
plt.ylabel("Frequency of occurrence")
