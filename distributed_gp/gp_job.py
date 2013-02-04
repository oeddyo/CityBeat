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



class GaussianProcessJob():

    def __init__(self, region, data_backward, current_time ,queue_server = 'tall4', days_to_predict = 1, data_source = 'instagram'):
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
        #try:
        print 'connecting to ',queue_server
        redis_conn = Redis(queue_server)
        self.q = Queue(connection = redis_conn)
        #except Exception as e:
        #    print 'Connecting to ',queue_server,'error'
        #    sys.exit(1)
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
        #print 'training'
        #print training
        #print 'testing'
        #print zip(testing, align, converted)
        #for tup in zip(result, converted):
        #    return_value.append( tup[0], str(tup[1]) )

        return result, converted




from utility.prediction_interface import PredictionInterface
from utility.prediction import Prediction
from utility.tool import getCurrentStampUTC

def test():
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    huge_region = Region(coordinates)
    
    regions = huge_region.divideRegions(25,25)
    filtered_regions = huge_region.filterRegions( regions )

    regions = filtered_regions
    print 'after filter ',len(regions)

    
    cur_utc_timestamp = getCurrentStampUTC()
    results = []

    for i in range(10):
        test_region = regions[i]
        gp = GaussianProcessJob(test_region, "1358273815",  "1359483415" )
        
        
        #try:
        res, pred_time = gp.submit( )
        results.append( (test_region, res, pred_time) )
        #except Exception as e:
        #    print 'Too few data, continue'
        #    continue
    
    save_results = [None]*len(results)
    gp_timeout = 1800
    done = False
    while not done:
        time.sleep(3)
        done = True
        time_dif = getCurrentStampUTC() - cur_utc_timestamp
        if time_dif > gp_timeout:
            print 'Timeout'
            break
        for result_pair in results:
            if result_pair[1].return_value is None:
                done = False
            else:
                result_idx = results.index(result_pair)
                if save_results[result_idx] == None:
                    save_results[ result_idx ] = (result_pair[0], result_pair[1].return_value, result_pair[2])
                    #save to mongo
                    to_save = save_results[result_idx]
                    region = to_save[0]
                    print 'to_save'
                    print to_save
                    for single_hour_prediction in zip(to_save[1], to_save[2]):
                        p = Prediction()
                        p.setRegion(region)
                        p.setModelUpdateTime(cur_utc_timestamp)
                        p.setPredictedValues( single_hour_prediction[0][0],single_hour_prediction[0][1])
                        p.setTime( str(single_hour_prediction[1]) )
                        p_json = p.toJSON()
                        print p_json
                        save_interface = PredictionInterface()
                        save_interface.saveDocument( p_json )
                            
#test()
