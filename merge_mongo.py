import pymongo

mongo = pymongo.Connection("grande",27017)
mongo_db1 = mongo['tmp_citybeat']
mongo_collection1 = mongo_db1.photos

mongo_db_dest_db = mongo['citybeat']
mongo_dest_collection = mongo_db_dest_db.photos

cnt = 0

for r in mongo_collection1.find():
    cnt+=1
    if(cnt%10000==0):
        print cnt
    r['_id'] = r['id']
    mongo_dest_collection.insert(r)
"""
for r in mongo_collection1.find():
    cnt+=1
    if(cnt%10000==0):
        print cnt
    mongo_dest_collection.insert(r)
"""
