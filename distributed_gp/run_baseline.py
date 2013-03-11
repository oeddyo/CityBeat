import time
import math
import sys

from datetime import datetime
from datetime import timedelta
import calendar
from uuid import uuid4


import pandas as pd
import numpy as np

from utility.instagram_time_series import InstagramTimeSeries
from utility.region import Region
from utility.config import InstagramConfig
from do_gp import Predict


from gp_job import GaussianProcessJob
from utility.tool import getCurrentStampUTC
from utility.tool import processAsPeopleCount

from utility.photo_interface import PhotoInterface


from utility.event_interface import EventInterface
from utility.event import Event



class Alarm():
    def __init__(self, region, start_time, end_of_time, candidate_collection):
        self.cur_time = int(start_time)
        self.end_of_time = int(end_of_time)
        self.region = region
        self.candidate_collection = candidate_collection
        
        self.training_start_time = self.cur_time - 24*3600*14 
        self.training_end_time = self.cur_time 
        self.means, self.stds = self._computeVariation()

    def _computeVariation(self):
        values = [0]*24
        ts = InstagramTimeSeries(self.region, self.training_start_time, self.training_end_time)
        instagram_ts = ts.buildTimeSeries()
        M = np.zeros([1000,24])
        initial_date = instagram_ts.index[0]
        for idx in instagram_ts.index:
            if not pd.isnull( instagram_ts[idx] ):
                day_dif = (idx - initial_date).days
                M[day_dif, idx.hour] = instagram_ts[idx]
        max_day = (instagram_ts.index[len(instagram_ts)-1] - initial_date ).days

        M = M[0:max_day, :]
        return np.mean(M, axis=0), np.std(M,axis=0)


    def _getFiftenMiniutesPhotos(self):
        pi = PhotoInterface('citybeat', 'photos_no_duplicate')
        _fifteen_minutes_ago = 15*60
        cursor  = pi.rangeQuery( self.region , (str( self.cur_time - _fifteen_minutes_ago), str(self.cur_time)) )
        _photos = []
        for p in cursor:
            _photos.append( p )
        _photos = sorted( _photos, key=lambda k:k['created_time'] )
        before = len(_photos)
        _photos = processAsPeopleCount(_photos)
        after = len(_photos)
        self.current_value = after
        self.photos = _photos

    def nextTimeStep(self, step_length ):
        _cur_time = self.cur_time + step_length
        if _cur_time > self.end_of_time:
            return False
        else:
            self.cur_time = _cur_time
            return True
    
    def fireAlarm(self):
        self._getFiftenMiniutesPhotos() #get current_value
        cur_hour = datetime.utcfromtimestamp(float(self.cur_time)).hour
        #print 'cur_hour = ',cur_hour, 'time = ',self.cur_time 
        mu = self.means[cur_hour]/4.0
        std = self.stds[cur_hour]/4.0
        #print 'mu is ',mu, 'std is ',std, 'cur_value = ',self.current_value
        zscore = (self.current_value - mu)*1.0/std

        if zscore > 3 and self.current_value>=8:
            e = Event()
            e.setPredictedValues(mu, std)
            e.setZscore(zscore)
            e.setRegion(self.region)
            e.setCreatedTime(self.cur_time)
            e.setActualValue(self.current_value)

            for p in self.photos:
                e.addPhoto(p)
        
            ei = EventInterface( )
            ei.setCollection(self.candidate_collection)
            #print datetime.utcfromtimestamp(float(e.getEarliestPhotoTime())), datetime.utcfromtimestamp(float(e.getLatestPhotoTime()))
            #print e.getEarliestPhotoTime(),e.getLatestPhotoTime()
            #print e.toJSON()['region']
            ei.addEvent(e)
            #ei.addEventWithoutMerge(e)
            # modified by xia

def run():
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    huge_region = Region(coordinates)
    
    alarm_region_size = 25

    regions = huge_region.divideRegions(alarm_region_size,alarm_region_size)
    filtered_regions = huge_region.filterRegions(regions, m = 25, n = 25)
    # get the same regions as in db. Here it's 10 by 10

    regions = filtered_regions
    print 'all regions',len(regions)
    region_cnt = 0
    cnt = 0
    for region in regions:
        print 'region_cnt ', region_cnt
        region_cnt+=1
        #delete the last 7*24*3600 to set it back to Dec 1st
        start_of_time =  1354320000 
        end_of_time = 1354320000 + 7*24*3600 
        alarm = Alarm(region, start_of_time, end_of_time ,'baseline_candidate_events' ) 
        region.display()
        
        while alarm.nextTimeStep(300):
            alarm.fireAlarm()
            cnt+=1
            if cnt%100==0:
                print 'cur = ', time.gmtime(float(alarm.cur_time) )
        print '\n\n' 

if __name__ == "__main__":
    run()                            
