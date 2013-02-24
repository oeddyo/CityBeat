import pymongo
import ntplib,datetime
from pandas import Series
from pandas import isnull
from datetime import datetime

from math import sqrt

def get_photos(mid_lat, mid_lng):
    mongo = pymongo.Connection("grande",27017)
    mongo_db = mongo['tmp_citybeat']
    mongo_collection = mongo_db.photos
    res = []
    repeat_filter = set()
    dates = []
    counts = []
    for p in mongo_collection.find({"mid_lat":mid_lat, "mid_lng":mid_lng}):
        if p['id'] in repeat_filter:
            continue
        repeat_filter.add(p['id'])
        res.append(p)
        dates.append( datetime.utcfromtimestamp(float(p['created_time'])))
        print datetime.utcfromtimestamp(float(p['created_time']))
        counts.append(1)
    ts = Series(counts, index = dates)
    print ts.index
    ts = ts.resample('10Min',how='sum', label='right')
    return ts, res 

def get_prediction(mid_lat, mid_lng):
    mongo = pymongo.Connection("grande",27017)
    mongo_db = mongo['test_predict']
    mongo_collection = mongo_db.prediction
    res = []
    for p in mongo_collection.find({"mid_lat":mid_lat, "mid_lng":mid_lng}):
        res.append(p)
    return res 

def total_seconds(delta):
    return delta.days*24*3600 + delta.seconds

def main():
    x = ntplib.NTPClient()
    ts, photos = get_photos("40.728072", "-73.9931535")
    print ts 
    sz = len(ts)
    cur_value = 0
    if sz>0:
        cur_time = ts.index[len(ts.index)-1]
        if isnull(ts.values[len(ts.values)-1]):
            cur_value = -1
        else:
            cur_value = ts.values[len(ts.values)-1]
    else:
        print 'error'
    predictions =  get_prediction(40.728072, -73.9931535)
    
    delta = cur_time - predictions[0]['time']
    
    for p in predictions:
        if( total_seconds( p['time'] - cur_time) < 3600):
            predict = p
            break
    
    print predict['mu']
    should_be = float(predict['mu'])/6.0+3*sqrt(float(predict['var']))/6.0
    print float(predict['mu'])/6.0, sqrt(float(predict['var']))/6.0, 'should be ',should_be,'real-> ',cur_value


main()


#get current time t
#for the current time t, get how many photos are really there
#search grande mongo - predict.prediction, and check how many photos should be there
#compute z score 
#fire an alarm if z>3.0
