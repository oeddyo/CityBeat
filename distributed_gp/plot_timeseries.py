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
    
    regions = filtered_regions
    test_cnt = 0
    print 'all regions',len(regions)
    for region in regions:
        #delete the last 7*24*3600 to set it back to Dec 1st
        start_of_time =  1354320000 + 7*24*3600
        end_of_time = 1354320000 + 7*24*3600 + 7*24*3600
        series =  InstagramTimeSeries( region, start_of_time, end_of_time)
        series =  series.buildTimeSeries()
        print series

if __name__ == "__main__":
    run()                            
