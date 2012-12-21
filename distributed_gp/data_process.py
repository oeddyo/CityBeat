"""
from lib.mysql_connect import connect_to_mysql

cursor = connect_to_mysql()
sql = "select * from herenow_region where time > '2012-10-08 6:00:00' and time < '2012-10-08 6:15:00';"
cursor.execute(sql)

print 'data:['
for r in cursor.fetchall():
    print '{'+'lat: '+str(r['mid_lat']) + ', lng:'+str(r['mid_lng']) + ', count: '+str(r['herenow']) + '},',
print ']'
"""

import pymongo
import pandas as pd
from pandas import Series
from datetime import datetime

def find_photos_given_region(lat, lng):
    mongo = pymongo.Connection("grande", 27017)
    mongo_db = mongo['production']
    mongo_collection = mongo_db.photos
    dates = []
    counts = []
    seen = set()
    for p in mongo_collection.find({"mid_lat":str(lat), "mid_lng":str(lng)}):
        if p['id'] in seen:
            continue
        seen.add( p['id'])
        dates.append(datetime.utcfromtimestamp(float(p['created_time'])))
        counts.append(1)
    ts = Series(counts, index = dates)
    ts = ts.resample('h',how='sum')
    print 'processing data...'
    return ts

#find_photos_given_region(40.750542,-73.9863145)


"for each mid_lat, mid_lng, read all the photos from there"
"organize it in pandas and add it into the job queue"




