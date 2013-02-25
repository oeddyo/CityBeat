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

from do_gp import Predict



class GaussianProcessJob():

    def __init__(self, region, data_backward, current_time , redis_queue, days_to_predict = 1, data_source = 'instagram'):
        """For a single gp job, specify its
        region - data structure that'specified by a box of lat, lng in region.py
        data_backward - timestamp for how long the time-series goes back
        queue_server - the redis server in rq. Note rq is a queue library
        days_to_predict - number of days to predict forward. Default is 1 day, do not change if unnecessary

        """
        self.current_time = current_time
        self.data_backward = data_backward
        self.region = region
        self.days_to_predict = days_to_predict
        self.data_source = data_source
        self._id = unicode(uuid4())
        
        #redis_conn = Redis(queue_server)
        #self.q = Queue(connection = redis_conn)
        self.q = redis_queue
        self.ts = self._getTimeSeries()

        if len(self.ts.index)>10:
            self.enough_data = True
        else:
            self.enough_data = False

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
        #ts = self._getTimeSeries()
        ts = self.ts
        index = ts.index
        if(len(index) < 3 ):
            raise Exception("Only %d data points"%(len(index)))
        start_date = ts.index[0]
        #notice here start_time is datetime object

        """Notice training here is in the format of
        (days from begining of the timeseries, number of data at that time)
        
        """
        training = []                  
        for idx in index:
            days_diff = (idx - start_date).days + (idx - start_date).seconds/(24*3600.0)
            training.append( (days_diff, ts[idx]) )
        nearest_current_date = index[-1]

        testing = []
        align = []
        converted_align = []
        for hour in range(25*self.days_to_predict):
            next_date = nearest_current_date + timedelta(seconds=3600*(hour+1))
            delta = next_date - start_date
            days_from_start = (delta.seconds+delta.days*86400)/(3600*24.0)
            testing.append( days_from_start)
            align.append( next_date )
            converted_align.append( calendar.timegm(next_date.utctimetuple()) ) 

        return training, testing, align, converted_align
    
    def getID(self):
        return self._id

    def submit(self):
        """submit this gaussian process to the queue and return the result
        object. The returned result is in the format of 
        (mean, variance, timestamp of the prediction)
        """
        training, testing, align, converted = self._dataPrepare()

        result = self.q.enqueue_call( Predict,args = ( training,testing, self._id,), timeout=86400, result_ttl=-1)
        print 'training '
        print self.ts.index
        print align
        print converted

        return result, converted

