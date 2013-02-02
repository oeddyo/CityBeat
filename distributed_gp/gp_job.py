import time
import math
import sys

from datetime import datetime
from datetime import timedelta
from itertools import count
import calendar

from utility.instagram_time_series import InstagramTimeSeries
from utility.region import Region
from utility.config import InstagramConfig
from  utility.photo_interface import PhotoInterface
from rq import Queue, Connection
from redis import Redis

from do_gp import Predict



class GaussianProcessJob():
    _ids = count(0)

    def __init__(self, region, data_backward, current_time, data_forward ,queue_server = 'tall4', days_to_predict = 1, data_source = 'instagram'):
        """For a single gp job, specify its
        region - data structure that'specified by a box of lat, lng in region.py
        data_backward - timestamp for how long the time-series goes back
        data_forward  - timestamp for how long the prediction goes forward
        queue_server - the redis server in rq. Note rq is a queue library

        """
        self.id = self._ids.next()
        self.current_time = current_time
        self.data_backward = data_backward
        self.data_forward = data_forward
        self.region = region
        self.days_to_predict = days_to_predict
        self.data_source = data_source
        #try:
        redis_conn = Redis(queue_server)
        self.q = Queue(connection = redis_conn)
        #except Exception as e:
        #    print 'Connecting to ',queue_server,'error'
        #    sys.exit(1)
    
    def _getTimeSeries(self):
        if self.data_source == 'instagram':
            its = InstagramTimeSeries(self.region, self.data_backward, self.current_time)
        elif self.data_source == 'twitter':
            pass
        ts = its.buildTimeSeries()
        return ts

    def _dataPrepare(self):
        """This is to return the 'future data points' that you want to
        predict. e.g. predict for each hour tomorrow how many people will
        show up at Times Square

        """
        ts = self._getTimeSeries()
        
        
        index = ts.index
        
        if(len(index) < 3 ):
            raise Exception("Too few data points")
        
        start_date = ts.index[0]
        #notice here start_time is datetime object

        """Notice training here is in the format of
        (days from begining of the timeseries, number of data at that time)
        
        """
        training = []                  
        for idx in index:
            days_diff = (idx - start_date).days + (idx - start_date).seconds/(24*3600.0)
            training.append( (days_diff, ts[idx]) )
        nearest_current_date = index[-2]

        testing = []
        align = []
        converted_align = []
        for hour in range(24*self.days_to_predict):
            next_date = nearest_current_date + timedelta(seconds=3600*(hour+1))
            delta = next_date - start_date
            days_from_start = (delta.seconds+delta.days*86400)/(3600*24.0)
            testing.append( days_from_start)
            align.append( next_date )
            converted_align.append( calendar.timegm(next_date.utctimetuple()) ) 

        return training, testing, align, converted_align

    def submit(self):
        """submit this gaussian process to the queue and return the result
        object

        """
        training, testing, align, converted = self._dataPrepare()
        
        #print training
        #print testing
        #print align
        #print converted
        result = self.q.enqueue_call( Predict,args = ( training,testing, self.id,), timeout=1720000, result_ttl=-1)

        return result

def test():
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    huge_region = Region(coordinates)
    regions = huge_region.divideRegions(10,10)
    test_region = regions[0]
    pi = PhotoInterface()
    photos = pi.rangeQuery(test_region, period = ("1353133815", "1355765815") )
    
    cur_utc_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())

    
    results = []

    for i in range(5):
        test_region = regions[i]
        gp = GaussianProcessJob(test_region, "1357273815",  str(cur_utc_timestamp), "1353778615" )
        res = gp.submit( )
        results.append( res )
    print results 
    save_results = [0]*len(results)
    done = False
    while not done:
        done = True
        for result in results:
            if result.return_value is None:
                done = False
            else:
                save_results[ results.index(result) ] = result.return_value
    for r in save_results:
        print r
test()
