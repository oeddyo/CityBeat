import pymongo
import calendar
import time
mongo = pymongo.Connection("grande",27017)

mongo_db_dest_db = mongo['citybeat']
mongo_dest_collection = mongo_db_dest_db.photos

cnt = 0

users = {}
unique_ids = set()


times = []

for r in mongo_dest_collection.find():
    #{"mid_lat":"40.750542", "mid_lng":"-73.9931535"}):
    cnt+=1
    if r['id'] in unique_ids:
        continue
    else:
        unique_ids.add(r['id'])
    if(cnt%10000==0):
        print cnt
    u_id = r['user']['id']
    
    times.append(r['created_time'])
    """    
    if u_id in users:
        users[u_id]+=1
    else:
        users[u_id] = 1
    """
times = sorted(times)
for t in times:
    print time.gmtime(float(t) )


print 'all ',len(users)
for v in users.values():
    print v


"""
for r in mongo_collection1.find():
    cnt+=1
    if(cnt%10000==0):
        print cnt
    mongo_dest_collection.insert(r)
"""
