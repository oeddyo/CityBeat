import time
import math
import sys

from datetime import datetime
from datetime import timedelta
import calendar
from uuid import uuid4


from utility.instagram_time_series import InstagramTimeSeries
from utility.region import Region
from utility.config import InstagramConfig
from rq import Queue, Connection
from redis import Redis
from do_gp import Predict


from gp_job import GaussianProcessJob
from utility.prediction_interface import PredictionInterface
from utility.prediction import Prediction
from utility.tool import getCurrentStampUTC

from utility.tool import processAsPeopleCount

from utility.photo_interface import PhotoInterface


from utility.event_interface import EventInterface
from utility.event import Event


class VarianceCompute():
    def __init__(self, region, start_time, end_of_time):
        self.start_time= int(start_time)
        self.end_of_time = int(end_of_time)
        self.region = region
    
    def _computeVariation(self):
        values = [0]*24
        ts = InstagramTimeSeries(self.region, self.start_time, self,end_of_time)
        instagram_ts = ts.buildTimeSeries()

        print instagram_ts


def run():
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    huge_region = Region(coordinates)
    
    alarm_region_size = 25

    regions = huge_region.divideRegions(alarm_region_size,alarm_region_size)
    filtered_regions = huge_region.filterRegions( regions, test = True)
    # get the same regions as in db. Here it's 10 by 10

    regions = filtered_regions
    test_cnt = 0
    print 'all regions',len(regions)
    

    for region in regions:
        #delete the last 7*24*3600 to set it back to Dec 1st
        start_of_time =  1354320000 
        end_of_time = 1354320000 + 7*24*3600 
        var = VarianceCompute(region, start_of_time, end_of_time)
        var._computeVariation() 
        
        """
        region.display()
        xia_cnt = 0
        while alarm.nextTimeStep(300):
            cnt += 1
            alarm.fireAlarm()
            if cnt%100==0:
                print 'cur = ', time.gmtime(float(alarm.cur_time) )
                print 'alarm = ',cnt
        print '\n\n' 
        """


class Alarm():
    def __init__(self, region, start_time, end_of_time, prediction_collection, candidate_collection):
        self.cur_time = int(start_time)
        self.end_of_time = int(end_of_time)
        self.region = region
        self.prediction_collection = prediction_collection
        self.candidate_collection = candidate_collection
    

    def _computeVariation(self, region):
        # for a geo location region, compute its mean, variance for each hour
        values = [0]*24


    def getNearestPrediction(self):
        pi = PredictionInterface()
        pi.setDB('citybeat')
        pi.setCollection(self.prediction_collection)
        return pi.getNearestPrediction(self.region, str(self.cur_time))

    def _getFiftenMiniutesPhotos(self):
        pi = PhotoInterface('citybeat', 'photos')
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
        prediction = self.getNearestPrediction()
        
        self._getFiftenMiniutesPhotos()
        if prediction is None:
            print 'None data for this region: details as follow'
            self.region.display()
            print 'time:' ,self.cur_time
            return 
        mu = float(prediction['mu'])/4.0
        std = float(prediction['std'])/4.0
        time_stamp = prediction['time']

        zscore = (self.current_value - mu)*1.0/std


        if zscore > 3:
            e = Event()
            e.setPredictedValues(mu, std)
            e.setZscore(zscore)
            e.setRegion(self.region)
            e.setCreatedTime(self.cur_time)
            e.setActualValue(self.current_value)

            for p in self.photos:
                e.addPhoto(p)
            #print 'current value ',4.0*self.current_value, ' predict = ',mu*4.0,' std = ',std*4.0
        
            ei = EventInterface( )
            ei.setCollection(self.candidate_collection)
            print e.getEarliestPhotoTime(),e.getLatestPhotoTime()
            #print e.toJSON()['region']
            #ei.addEvent(e)
            ei.addEventWithoutMerge(e)
            # modified by xia


if __name__ == "__main__":
    run()                            
