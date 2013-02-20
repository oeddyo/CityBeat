#Edited by: Chaolun Xia, 2013-Jan-09#

from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface

import pymongo
import ntplib,datetime
from pandas import Series
from pandas import isnull
from datetime import datetime
import calendar
from math import sqrt
import time
from data_process import find_photos_given_region

def get_prediction(mid_lat, mid_lng):
    mongo = pymongo.Connection("grande",27017)
    mongo_db = mongo['predict']
    mongo_collection = mongo_db.prediction
    res = []
    cnt = 24
    for p in mongo_collection.\
            find({"mid_lat":mid_lat, "mid_lng":mid_lng}).\
            sort('model_update_time',-1):                       #use sort here to get latest model predicitons
        res.append(p)
        cnt-=1
        if cnt==0:
            break
    res = sorted( res, key = lambda x:x['time'])
    return res 

def total_seconds(delta):
    return delta.days*24*3600 + delta.seconds

def read_regions():
    res = []
    for l in open('number.csv','r').readlines():
        t = l.split(',')
        res.append( (t[0],t[1]) )
    res.reverse()
    return res

def save_to_mongo(to_save):
    mongo = pymongo.Connection("grande",27017)
    mongo_db = mongo['server']
    mongo_collection = mongo_db.heatmap
    
    mongo_collection.update(  {'mid_lat':to_save['mid_lat'], 'mid_lng':to_save['mid_lng']}, to_save, True )
    """
    {
    mid_lat:xxx,
    mid_lng:xxx,
    predict: xxxx,
    real_count: xx,
    var: xxx,
    photos: [p1,p2...],
    zscore: xxx,
    }
    """

def main():
	
	  # inintialize the database for storing the alarms
    myDB = MongoDBInterface('grande', 27017)
    myDB.SetDB('alarm_filter')
    myDB.SetCollection('photos')
    
    adi = AlarmDataInterface()
    
    regions = read_regions()
    

    for region in regions:
        to_save = {'mid_lat':region[0], 'mid_lng':region[1], 'valid':False, 'real_count':-1,'mu':-1, 'std':-1, 'photos':[], 'zscore':-1};
        photos = []
        try:
            ts, photos = find_photos_given_region(region[0], region[1], '15Min', 'tmp_citybeat', True)
        except Exception as e:
            save_to_mongo(to_save)
            continue
        sz = len(ts)
        cur_value = 0
        if sz>0:
            cur_time = ts.index[len(ts.index)-1]
            if isnull(ts.values[len(ts.values)-1]):
                cur_value = -1
            else:
                cur_value = ts.values[len(ts.values)-1]
        else:
            save_to_mongo(to_save)
            continue
        if total_seconds(datetime.utcnow() - cur_time)>900:
            # there's no latest photo at this region
            save_to_mongo(to_save)
            continue

        try:
            predictions =  get_prediction(str(region[0]), str(region[1]))
        except Exception as e:
            save_to_mongo(to_save)
            continue
        predict = -1
        for p in predictions:
            seconds = total_seconds( p['time']-cur_time)
            if( seconds<=3600 and seconds>=0):
                #print 'p time is ',p['time'], 'cur_time is ',cur_time
                predict = p
        if predict==-1:
            save_to_mongo(to_save)
            continue
        
        mu = float(predict['mu'])/4.0
        std = sqrt(float(predict['var']))/4.0
        zscore = (cur_value - mu)/std

        within_range = float(predict['mu'])/4.0+3*sqrt(float(predict['var']))/4.0
        
        photos_to_save = []
        for photo in photos:
            delta = total_seconds( cur_time - datetime.utcfromtimestamp( float(photo['created_time'])) )
            if delta>=0 and delta<=900:
            	photo['label'] = 'unlabeled'
            	photos_to_save.append(photo)

        to_save['photos'] = photos_to_save
        to_save['real_count'] = cur_value
        to_save['valid'] = True
        to_save['std'] = sqrt(float(predict['var']))/4.0
        to_save['mu'] = float(predict['mu'])/4.0
        to_save['zscore'] = zscore
        save_to_mongo(to_save) 
        

        if zscore>=2.0 and cur_value>=3:
            print datetime.utcnow()
            print region[0],",",region[1]
            print float(predict['mu'])/4.0, sqrt(float(predict['var']))/4.0, 'range ',within_range,'real-> ',cur_value
            for photo in photos_to_save:
                print 'printing photos: ', photo['link'], photo['created_time'], photo['id'], datetime.utcfromtimestamp(float(photo['created_time']))
            
            #group photos into an unlabeled event and save it to the db  
            predicted_mu = float(predict['mu'])/4.0
            predicted_std = sqrt(float(predict['var']))/4.0
            newEvent = {'created_time':datetime.utcnow(), 'mid_lat':region[0], 'mid_lng':region[1], 'predicted_mu':predicted_mu, 'predicted_std':predicted_std, 'actual_value':cur_value, 'zscore':zscore, 'photos':photos_to_save, 'label':'unlabeled'}
            	
            if not adi.MergeEvent(newEvent):
            	print 'created an event'
            	myDB.SaveItem(newEvent)
            else:
            	print 'merged an event'
            print '\n'
            	
            
            

main()


#get current time t
#for the current time t, get how many photos are really there
#search grande mongo - predict.prediction, and check how many photos should be there
#compute z score 
#fire an alarm if z>3.0
