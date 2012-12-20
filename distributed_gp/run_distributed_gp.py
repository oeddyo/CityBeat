import os
from rq import Queue, Connection
#from test import haha
from do_gp import Predict 
from redis import Redis
import time
from random import randrange
from data_process import find_photos_given_region
from datetime import timedelta
from datetime import datetime
import pymongo
import calendar 

def read_regions():
    f = open('number.csv','r')
    res = []
    for line in f.readlines():
        t = line.split(',')
        res.append((t[0], t[1]))
    res.reverse()
    #return res
    #return [(40.728072, -73.9931535), (40.75953,-73.9863145), (40.746048, -73.9931535), (40.741554,-73.9931535),  (40.75953, -73.9794755), (40.755036, -73.9794755)]
    return [(40.728072,-73.9931535)]

def process_ts(ts):
    """return two results; the first is the start datetime, the second is the list of training data"""
    idx = ts.index
    start = idx[0]
    res = []
    for t in idx:
        days_diff = (t-start).days + (t-start).seconds/(24*3600.0);
        res.append((days_diff, ts[t]))
    return start, res

def get_testing(start, predict_days):
    cur = 1.0/24;
    res = []
    while(cur<predict_days):
        print cur+start
        res.append(cur+start)
        cur+=1.0/24
    return res

def save_to_mongo(result, region, model_update_time):
    mongo = pymongo.Connection("grande",27017)
    mongo_db = mongo['predict']
    mongo_collection = mongo_db.prediction
    for r in result:
        t = {'time':r[0], 'mu':r[1], 'var':r[2], 'mid_lat':region[0], 'mid_lng':region[1], 'model_update_time':model_update_time}
        mongo_collection.insert(t)

def fix_time(start, result_list):
    """re-align the time"""
    res = []
    for r in result_list:
        res.append( (start + timedelta(days = float(r[0])), float(r[1]), float(r[2])) )
    return res

def main():
    predict_days = 3
    regions = read_regions()
    redis_conn = Redis('tall4')
    q = Queue(connection=redis_conn)
    cnt = 0
    async_results = {}
    start_time = []
    model_update_time = datetime.utcnow()
    
    for region in regions:
        par = cnt
        try:
            ts = find_photos_given_region(region[0], region[1])
        except Exception as e:
            print e
            continue
        start, training = process_ts(ts)
        start_time.append(start)
        testing = get_testing(( ts.index[len(ts)-1] - start).days, predict_days)
        async_results[cnt] = q.enqueue_call( Predict, args = ( training,testing, cnt,), timeout=1720000, result_ttl=-1 )
        cnt+=1
    done = False
    begin_time = time.time()
    time.sleep(2)
    saved_flag = [0]*len(async_results)
    while not done:
        print "Time elapsed : ",time.time()-begin_time
        done = True
        for x in range(cnt):
            print 'checking ',x
            result = async_results[x].return_value
            print 'check done'
            print 'res is ',result
            if result is None:
                done = False
                continue
            if saved_flag[x] == 0:
                result = fix_time(start_time[x], result) 
                save_to_mongo(result, regions[x], model_update_time)
                saved_flag[x] = 1
        time.sleep(0.2)

main() 
