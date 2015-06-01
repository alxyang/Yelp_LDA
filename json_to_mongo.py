import time
import json
from pymongo import MongoClient
import Config

db = MongoClient(Config.MONGO_CONNECTION_URL)[Config.ACADEMIC_DATASET_DB]
reviews_collection = db[Config.COLLECTION_REVIEWS]
business_collection = db[Config.COLLECTION_BUSINESSES]

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
                "_id": data["business_id"],
                "name": data["name"],
                "city": data["city"],
                "state": data["state"],
                "categories": data["categories"],
                "stars": data["stars"]
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
                    "review_id": data["review_id"],
                    "business_id": data["business_id"],
                    "text": data["text"],
                    "stars": data["stars"],
                    "votes": data["votes"]
                })

if __name__ == "__main__":
    if reviews_collection.count() > 0:
        print "dropping collection"
        reviews_collection.drop()
    if business_collection.count() > 0:
        print "dropping collection"
        business_collection.drop()

    t0 = time.time()
    print "Loading data..."
    dataset = Config.YELP_DATASET
    importBusinesses(dataset)
    importReviews(dataset)
    print "Done."
    print time.time() - t0, "seconds"

    review_count = db[Config.COLLECTION_REVIEWS].count()
    business_count = db[Config.COLLECTION_BUSINESSES].count()
    print "# review documents: ", review_count
    print "# business documents: ", business_count

