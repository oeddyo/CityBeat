import pymongo
def save_mogo(res, mid_lat, mid_lng):
    connection = pymongo.Connection("grande", 27017)
    db = connection.instagram
    for r in res:
        r['mid_lat'] = mid_lat
        r['mid_lng'] = mid_lng
        db.insert(r)
