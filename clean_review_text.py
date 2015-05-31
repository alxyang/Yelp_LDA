from pymongo import MongoClient
import nltk
import time
import string
import Config

db = MongoClient(Config.MONGO_CONNECTION_URL)[Config.ACADEMIC_DATASET_DB]
reviews_collection = db[Config.REVIEWS_COLLECTION]

# create new table for cleaned reviews, drop if exists
cleaned_reviews = db[Config.CLEANED_REVIEWS]
if cleaned_reviews.count() > 0:
    print "dropping collection"
    cleaned_reviews.drop()

def clean_data():
    stopwords = set(nltk.corpus.stopwords.words('english'))
    wnl = nltk.WordNetLemmatizer()

    counter = 0
    for r in reviews_collection.find():
        print counter
        cleaned_review_words = []

        # lower case and remove punctiation
        punctuation = set(string.punctuation)
        review_text = (''.join([c for c in r['text'].lower() if not c in punctuation]))
        # remove punctuation?

        sentences = nltk.sent_tokenize(review_text)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for w in words:
                if w not in stopwords:
                    # consider tagging POS, but decreases performance drastically
                    cleaned_review_words.append(wnl.lemmatize(w))

        cleaned_reviews.insert({
            "review_id": r["review_id"],
            "business_id": r["business_id"],
            "stars": r['stars'],
            "votes":r["votes"],
            "text": r["text"],
            "cleaned_text": cleaned_review_words
            })

        counter += 1

if __name__ == "__main__":
    t0 = time.time()
    print "Cleaning data..."
    clean_data()
    print "Done."
    print time.time() - t0, "seconds"


