from gensim  import models
from collections import defaultdict
from pymongo import MongoClient
from gensim import corpora
import nltk
import string
import Config

db = MongoClient(Config.MONGO_CONNECTION_URL)[Config.ACADEMIC_DATASET_DB]
cleaned_reviews = db[Config.CLEANED_REVIEWS]
businesses = db[Config.COLLECTION_BUSINESSES]

dictionary = corpora.Dictionary.load(Config.DICTIONARY_LOCAL)
lda = models.LdaModel.load(Config.LDA_LOCAL)
lsi = models.LsiModel.load('model.lsi')

def businesses_sorted_by_review_count():
    business_to_reviews = defaultdict(float)
    for r in cleaned_reviews.find():
       business_to_reviews[r['business_id']] += 1

    tmp = [(business_to_reviews[r], r) for r in business_to_reviews]
    tmp.sort()
    tmp.reverse()
    return tmp

def clean_review(review):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    wnl = nltk.WordNetLemmatizer()

    counter = 0
    cleaned_review_words = []

    # lower case and remove punctiation
    punctuation = set(string.punctuation)
    review_text = (''.join([c for c in review.lower() if not c in punctuation]))

    sentences = nltk.sent_tokenize(review_text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        for w in words:
            if w not in stopwords:
                # consider tagging POS, but decreases performance drastically
                cleaned_review_words.append(wnl.lemmatize(w))

    return cleaned_review_words

def find_topics_in_review_sort_by_percentage(cleaned_text):
    topics = lda[dictionary.doc2bow(cleaned_text)]

    sorted_percentage = [(x[1], x[0]) for x in topics]
    sorted_percentage.sort()
    sorted_percentage.reverse()

    return sorted_percentage

def find_topics_in_review(cleaned_text):
    topics = lda[dictionary.doc2bow(cleaned_text)]
    return topics


def find_positive_topics_for_business(businessId):
    counter = 0
    positive_topics_to_frequency = defaultdict(float)
    for r in cleaned_reviews.find({"business_id": businessId}):
        # check and handle review rating
        # clean review topics to only take those above 6%
        if r['stars'] > 3.5:
            for topic_id, percentage in find_topics_in_review(r['cleaned_text']):
                if percentage > 0.06:
                    positive_topics_to_frequency[topic_id] += 1
        counter += 1

    tmp = [(positive_topics_to_frequency[t], t) for t in positive_topics_to_frequency]
    tmp.sort()
    tmp.reverse()

    print "# reviews found for this business", counter
    for frequency, topic_id in tmp[:10]:
        print str(frequency) + "\t" + lda.print_topic(topic_id)

    return tmp

def find_negative_topics_for_business(businessId):
    counter = 0
    negative_topics_to_frequency = defaultdict(float)
    for r in cleaned_reviews.find({"business_id": businessId}):
        # check and handle review rating
        if r['stars'] < 3:
            for topic_id, percentage in find_topics_in_review(r['cleaned_text']):
                # clean review topics to only take those above 6%
                if percentage > 0.06:
                    negative_topics_to_frequency[topic_id] += 1
        counter += 1

    tmp = [(negative_topics_to_frequency[t], t) for t in negative_topics_to_frequency]
    tmp.sort()
    tmp.reverse()

    print "# reviews found for this business", counter
    for frequency, topic_id in tmp[:10]:
        print str(frequency) + "\t" + lda.print_topic(topic_id)

    return tmp

def display_prediction(review):
    cleaned_text = clean_review(review)
    sorted_topics = find_topics_in_review_sort_by_percentage(cleaned_text)

    for percentage, topic_number in sorted_topics:
        print str(round(percentage * 100, 2)) + "%" + "\t T:" + str(topic_number) + "\t" + lda.print_topic(topic_number)

def get_business_info(business_id):
    for r in businesses.find({"_id": business_id}):
        print "business name" + "\t" + r['name']
        print "state" + "\t" + r['state']
        print "city" + "\t" + r['city']
        print "rating" + "\t" + str(r['stars'])
        print r['categories']
        return r


# predicts all topics for a given business, separated by rating
def find_all_topics_for_business(businessId):
    counter = 0
    topics_to_frequency = defaultdict(float)
    for r in cleaned_reviews.find({"business_id": businessId}):
        # check and handle review rating
        # clean review topics to only take those above 6%
        for topic_id, percentage in find_topics_in_review(r['cleaned_text']):
            #if percentage > 0.06:
            topics_to_frequency[topic_id] += percentage
        counter += 1

    tmp = [(topics_to_frequency[t], t) for t in topics_to_frequency]
    tmp.sort()
    tmp.reverse()

    #print "# reviews found for this business", counter
    #for frequency, topic_id in tmp[:10]:
        #print str(frequency) + "\t" + lda.print_topic(topic_id)

    topics = [x[1] for x in tmp[:10]]
    return topics

def max_jaccard(bid, t1):
    b1 = get_business_info(bid)

    t1 = set(t1)
    max_jaccard = 0.0
    max_jaccard_set = set()
    counter = 0

    for b2 in businesses.find():
        print counter
        counter += 1
        if b1['_id'] == b2['_id']:
            continue

        if b1['city'] != b2['city']:
            continue

        #if b2['city'] != 'La Jolla':
            #continue

        t2 = set(find_all_topics_for_business(b2['_id']))
        jaccard_similarity = (len(t1.intersection(t2)) * 1.0)/len(t1.union(t2))
        if jaccard_similarity > max_jaccard:
            max_jaccard = jaccard_similarity
            max_jaccard_set.clear()
        if jaccard_similarity == max_jaccard:
            max_jaccard_set.add(b2['_id'])

    print max_jaccard_set
    print max_jaccard

    for bid in max_jaccard_set:
        get_business_info(bid)

if __name__ == "__main__":
    #print "positive topics"
    #find_positive_topics_for_business('qHmamQPCAKkia9X0uryA8g')

    #print "negative topics"
    #find_negative_topics_for_business('qHmamQPCAKkia9X0uryA8g')

    #print "business info"
    #get_business_info('qHmamQPCAKkia9X0uryA8g')

    # get the businesses with the most reviews and their info
    #for _, bid in businesses_sorted_by_review_count()[:100]:
        #get_business_info(bid)

    # top dog
    #bid1 = 'qHmamQPCAKkia9X0uryA8g'

    # la burrito
    bid1 = 'q33FT8iYvU2UUbJuiEQWUw'

    # blondies pizza
    #bid1 = 'WqAtgHTxgS-B8J6iHc4eeA'
    t1 = find_all_topics_for_business(bid1)
    max_jaccard(bid1, t1)



