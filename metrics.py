import json

def importJSON(dataset):
    yelp_data = open(dataset)
    r = []
    b = []
    u = []
    for line in yelp_data:
        try:
            data = json.loads(line)
        except ValueError:
            print "Oops!"

        if data["type"] == "user":
            u.append(data)
        elif data["type"] == "business":
            b.append(data)
        elif data["type"] == "review":
            r.append(data)
    return r, b, u

if __name__ == "__main__":
    dataset = "yelp_academic_dataset.json"
    print "Loading data..."
    reviews, businesses, users = importJSON(dataset)
    print "Done."

    print "# of reviews", len(reviews)
    print "# of businesses", len(businesses)
    print "# of users", len(users)


