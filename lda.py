from nltk import WordNetLemmatizer
from pymongo import MongoClient
from nltk.corpus import stopwords
from gensim import corpora
import nltk
import gensim
import time
import Config

db = MongoClient(Config.MONGO_CONNECTION_URL)[Config.ACADEMIC_DATASET_DB]
cleaned_reviews = db[Config.CLEANED_REVIEWS]

# perform LDA
def lda(dictionary, mm):
    # takes about 70 minutes to run
    t0 = time.time()
    print "performing LDA"
    lda = gensim.models.LdaModel(corpus=mm, id2word=dictionary, num_topics=Config.TOPIC_NUM)
    lda.save(Config.LDA_LOCAL)
    print "Done."
    print time.time() - t0, "seconds"
    return lda

if __name__ == "__main__":
    t0 = time.time()
    print "Loading Dictionary"
    dictionary = corpora.Dictionary.load(Config.DICTIONARY_LOCAL)
    print "Done."
    print time.time() - t0, "seconds"

    t0 = time.time()
    print "Loading Corpus"
    mm = corpora.MmCorpus(Config.CORPUS_LOCAL)
    print "Done."
    print time.time() - t0, "seconds"

    # perform lda
    lda = lda(dictionary, mm)

    # write the topics to a file
    i = 0
    for topic in lda.show_topics(num_topics=Config.TOPIC_NUM):
        print '#' + str(i) + ': ' + topic
        i += 1
