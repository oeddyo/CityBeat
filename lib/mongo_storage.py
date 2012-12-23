import pymongo
def save_mogo(res, mid_lat, mid_lng, mongo_db_name):
    mongo = pymongo.Connection("grande", 27017)
    mongo_db = mongo[mongo_db_name]
    mongo_collection = mongo_db.photos
    for r in res:
        r['mid_lat'] = mid_lat
        r['mid_lng'] = mid_lng
        r['_id'] = r['id']
        mongo_collection.insert(r)
