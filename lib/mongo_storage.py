import pymongo
def save_mogo(res, mid_lat, mid_lng):
    mongo = pymongo.Connection("grande", 27017)
    mongo_db = mongo['instagram']
    mongo_collection = mongo_db.photos
    for r in res:
        r['mid_lat'] = mid_lat
        r['mid_lng'] = mid_lng
        mongo_collection.insert(r)
