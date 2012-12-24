import pymongo
import pandas as pd
from pandas import Series
from datetime import datetime

def find_photos_given_region(lat, lng, resample_freq, db_name, count_people = True):
    mongo = pymongo.Connection("grande", 27017)
    mongo_db = mongo[db_name]
    mongo_collection = mongo_db.photos
    dates = []
    counts = []
    seen = set()
    pre_date = {}       #for a single user, when is his last photo; this is used to avoid to count a user's taking many pics in a row
    photos = []
    
    for p in mongo_collection.find({"mid_lat":str(lat), "mid_lng":str(lng)}):
        if p['id'] in seen:
            continue
        seen.add(p['id'])
        photos.append( p )
    
    photos = sorted(photos, key = lambda x: x['created_time'])
    
    photos_return = []
    for p in photos:
        if count_people:
            user = p['user']['username'] 
            if user not in pre_date:
                pre_date[user] = p['created_time']
                photos_return.append( p )
                dates.append(datetime.utcfromtimestamp(float(p['created_time'])))
                counts.append(1)
            else:
                if float(p['created_time']) - float(pre_date[user]) >600:        # within 10 minutes count it as a single user
                    #print 'now ',p['created_time'], ' pre',pre_date[user]
                    pre_date[user] = p['created_time']
                    photos_return.append( p )
                    dates.append(datetime.utcfromtimestamp(float(p['created_time'])))
                    counts.append(1)
                else:
                    #print 'pre is ',datetime.utcfromtimestamp(float(pre_date[user])),' next is ',datetime.utcfromtimestamp(float(p['created_time']))
                    continue
        else: 
            dates.append(datetime.utcfromtimestamp(float(p['created_time'])))
            counts.append(1)
            photos_return.append(p)
    """ 
    for p in photos_return:
        print p['created_time'] , p['user']['username'], p['link']
    print '\n\n'
    """
    ts = Series(counts, index = dates)

    ts = ts.resample(resample_freq,how='sum', label='right')
    #print ts
    return ts, photos_return

find_photos_given_region(40.750542,-73.9863145, '10Min', 'tmp_citybeat', True)


"for each mid_lat, mid_lng, read all the photos from there"
"organize it in pandas and add it into the job queue"




