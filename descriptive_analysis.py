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

non_food = []
for b in businesses:
    flag = 0
    for c in b['categories']:
        if c == 'Food' or c=='Restaurants':
            flag = 1
    if flag == 0:
        non_food.append(b)

food_bus = set([b['business_id'] for b in food_related])
nf_bus = set([b['business_id'] for b in non_food])

food_pop = []
nf_pop = []
for c in review_count:
    if c in food_bus:
        food_pop.append([review_count[c], c])
    elif c in nf_bus:
        nf_pop.append([review_count[c], c])
    else:
        print "must be error somewhere"
        
        
x_to_y = defaultdict(int)
for c in nf_pop:
    x_to_y[c[0]] += 1

food_x_to_y = defaultdict(int)
for c in food_pop:
    food_x_to_y[c[0]] += 1
    
X = []
Y = []
for x in x_to_y:
    X.append(x)
    Y.append(x_to_y[x])

X_food = []
Y_food = []
for x in food_x_to_y:
    X_food.append(x)
    Y_food.append(food_x_to_y[x])

plt.subplot(211)
plt.plot(X, Y)
#plt.title("Number of reviews per business")
#plt.xlabel("Number of reviews")
#plt.ylabel("Frequency of occurrence")

plt.subplot(212)
plt.plot(X_food, Y_food)

plt.plot(X, Y, X_food, Y_food, 'r--')


  
for i in range(50):
    business_id = popularBusinesses[i][1]
    print "category:%s" %category[business_id], "count:%r" % popularBusinesses[i][0] 



#average number of words per review
rev_count = []
for r in reviews:
    rev_count.append(len(r['text'].split()))
rev_count.sort()
rev_count.reverse()

nf_rev_count = []
food_rev_count = []
for r in reviews:
    if r['business_id'] in food_bus:
        food_rev_count.append(len(r['text'].split()))
    elif r['business_id'] in nf_bus:
        nf_rev_count.append(len(r['text'].split()))
    else:
        print "mamamia"

numpy.median(numpy.array(rev_count))

x_to_y = defaultdict(int)
for c in rev_count:
    x_to_y[c] += 1

x_to_y = defaultdict(int)
for c in nf_rev_count:
    x_to_y[c] += 1

food_x_to_y = defaultdict(int)
for c in food_rev_count:
    food_x_to_y[c] += 1
    
X = []
Y = []
for x in x_to_y:
    X.append(x)
    Y.append(x_to_y[x])

X_food = []
Y_food = []
for x in food_x_to_y:
    X_food.append(x)
    Y_food.append(food_x_to_y[x])

plt.plot(X, Y, X_food, Y_food, 'r--')
plt.title("Number of words per review")
plt.xlabel("Number of words")
plt.ylabel("Frequency of occurrence")

X = []
Y = []
for x in x_to_y:
    X.append(x)
    Y.append(x_to_y[x])
    
plt.plot(X, Y)
plt.title("Number of words per review")
plt.xlabel("Number of words")
plt.ylabel("Frequency of occurrence")
