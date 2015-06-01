from pymongo import MongoClient
from gensim.models import LdaModel
from gensim import corpora
import Config

lda = LdaModel.load(Config.LDA_LOCAL)

if __name__ == "__main__":
    # write the topics to a file
    i = 0
    for topic in lda.show_topics(num_topics=Config.TOPIC_NUM):
        print '#' + str(i) + ': ' + topic
        i += 1
