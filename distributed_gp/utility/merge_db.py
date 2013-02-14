from event_interface import EventInterface

from prediction_interface import PredictionInterface

from region import Region

from bson.objectid import ObjectId
from event import Event

from datetime import datetime

def getDate(utc_time):
	return repr(datetime.fromtimestamp(int(utc_time)))

ei = EventInterface()
ei.setDB('citybeat')
ei.setCollection('next_week_candidate_event_25by25')

ei2 = EventInterface()
ei2.setDB('citybeat')
ei2.setCollection('next_week_candidate_event_25by25_merged')

events = ei.getAllDocuments().sort('created_time', 1)
for event in events:
	if event['actual_value']  >= 8 and event['zscore'] >= 3.0:
		ei2.addEvent(event)



#region= {'min_lat': 40.743583800000003, 'max_lng': -73.978088200000002, 'min_lng': -73.998103900000004, 'max_lat': 40.756847}
#utc_time = str(1354728300)<div style="text-align: left"></div>

#region = {'min_lat': 40.730320599999999, 'max_lng': -73.978088200000002, 'min_lng': -73.998103900000004, 'max_lat': 40.743583800000003}
#utc_time = str(1354340400)
#
#condition = ({'region.min_lat':region['min_lat'],
#		          'region.min_lng':region['min_lng'],
#		          'region.max_lat':region['max_lat'],
#		          'region.max_lng':region['max_lng']})
#
#predictions = pi.getAllDocuments(condition).sort('time', 1)
#for prediction in predictions:
#	t = int(prediction['time'])
#	print getDate(t)
##	print t
##	if t >= int(utc_time) and t - 3600 <= int(utc_time):
##		print 'good:', prediction['time']
#	
#query_time = 1354740900
#print getDate(query_time)
#
#print pi.getNearestPrediction(region, utc_time)