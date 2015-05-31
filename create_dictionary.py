from nltk import WordNetLemmatizer
from pymongo import MongoClient
from nltk.corpus import stopwords
from gensim import corpora
import nltk
import time
import Config

db = MongoClient(Config.MONGO_CONNECTION_URL)[Config.ACADEMIC_DATASET_DB]
cleaned_reviews = db[Config.CLEANED_REVIEWS]

# maps words to ids, NOT # of appearances
def createDictionary():
    t0 = time.time()
    print "Creating Dictionary"
    dictionary = corpora.Dictionary(review['cleaned_text'] for review in cleaned_reviews.find())
    dictionary.filter_extremes(keep_n=10000)
    dictionary.compactify()
    corpora.Dictionary.save(dictionary, Config.DICTIONARY_LOCAL)
    print "Done."
    print time.time() - t0, "seconds"
    return dictionary

# creates bag of word model
def createCorpus(dictionary):
    t0 = time.time()
    print "converting Documents to Bag of Words vectors..."
    corpus = [dictionary.doc2bow(review['cleaned_text']) for review in cleaned_reviews.find()]
    corpora.MmCorpus.serialize(Config.CORPUS_LOCAL, corpus)
    print "Done."
    print time.time() - t0, "seconds"
    return corpus

if __name__ == "__main__":
    dictionary = createDictionary()
    corpus = createCorpus(dictionary)

    t0 = time.time()
    print "Loading Dictionary"
    local_dictonary = corpora.Dictionary.load(Config.DICTIONARY_LOCAL)
    print "Done."
    print time.time() - t0, "seconds"

    t0 = time.time()
    print "Loading Corpus"
    local_corpus = corpora.MmCorpus(Config.CORPUS_LOCAL)
    print "Done."
    print time.time() - t0, "seconds"
