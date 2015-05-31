import os
import time
import json
import Config
from pymongo import MongoClient

db = MongoClient(Config.MONGO_CONNECTION_URL)[Config.ACADEMIC_DATASET_DB]
reviews_collection = db[Config.REVIEWS_COLLECTION]
business_collection = db[Config.BUSINESS_COLLECTION]

def importBusinesses(dataset):
    yelp_data = open(dataset)
    for line in yelp_data:
        try:
            data = json.loads(line)
        except ValueError:
            print "Oops!"

        #users not considered
        if data["type"] == "business" and 'Restaurants' in data["categories"]:
            business_collection.insert({
                "_id": data["business_id"]
                })

def importReviews(dataset):
    yelp_data = open(dataset)
    for line in yelp_data:
        try:
            data = json.loads(line)
        except ValueError:
            print "Oops!"

        if data["type"] == "review":
            is_restaurant = business_collection.find({"_id": data["business_id"]}).count()
            if is_restaurant > 0:
                reviews_collection.insert({
                    "reviewId": data["review_id"],
                    "business": data["business_id"],
                    "text": data["text"],
                    "stars": data['stars'],
                    "votes":data["votes"]
                })

if __name__ == "__main__":
    t0 = time.time()
    print "Loading data..."
    dataset = Config.YELP_DATASET
    importBusinesses(dataset)
    importReviews(dataset)
    print "Done."
    print time.time() - t0, "seconds"

    review_count = db[Config.REVIEWS_COLLECTION].count()
    business_count = db[Config.BUSINESS_COLLECTION].count()
    print "# review documents: ", review_count
    print "# business documents: ", business_count

