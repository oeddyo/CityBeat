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


from utility.photo_interface import PhotoInterface

class Alarm():
    def __init__(self, region, start_time, end_of_time):
        self.cur_time = float(start_time)
        self.end_of_time = float(end_of_time)
        self.region = region

    def getNearestPrediction(self):
        pi = PredictionInterface()
        pi.setDB('citybeat')
        pi.setCollection('prediction_10by10')
        return pi.getNearestPrediction(self.region, str(self.cur_time))

    def _getFiftenMiniutesPhotos(self):
        pi = PhotoInterface()
        _fifteen_minutes_ago = 15*60
        cursor  = pi.rangeQuery( region , (str( self.cur_time - _fifteen_minutes_ago), str(self.cur_time)) )
        _photos = []
        for p in cursor:
            _photos.append( p )
        its = InstagramTimeSeries(self.region, str(self.cur_time), str(self.cur_time) , '15Min')
        ts = its.buildTimeSeries()
        print ts


    def nextFifteenMiniutes(self):
        _cur_time = self.cur_time + 15*60
        if _cur_time > self.end_of_time:
            return False
        else:
            self.cur_time = _cur_time
            return True
def run():
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    huge_region = Region(coordinates)
    
    regions = huge_region.divideRegions(10,10)
    filtered_regions = huge_region.filterRegions( regions, test = True )
    # get the same regions as in db. Here it's 10 by 10
    regions = filtered_regions


    for region in regions:
        start_of_time =  1354320000
        end_of_time = 1354320000 + 30*24*3600
        alarm = Alarm(region, start_of_time, end_of_time)
        while alarm.nextFifteenMiniutes():
            alarm._getFiftenMiniutesPhotos()


    
if __name__ == "__main__":
    run()                            
