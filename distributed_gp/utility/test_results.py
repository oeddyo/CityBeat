from event_interface import EventInterface

from prediction_interface import PredictionInterface

from region import Region

from bson.objectid import ObjectId
from event import Event

from datetime import datetime

def getDate(utc_time):
	return repr(datetime.fromtimestamp(int(utc_time)))

ei = EventInterface()
ei.setCollection('candidate_event_10by10')

ei2 = EventInterface()
ei2.setCollection('candidate_event_10by10_merged')

events = ei.getAllDocuments().sort('created_time', 1)
for event in events:
	if len(event['photos']) >= 10:
		ei2.addEvent(event)



#region= {'min_lat': 40.743583800000003, 'max_lng': -73.978088200000002, 'min_lng': -73.998103900000004, 'max_lat': 40.756847}
#utc_time = str(1354728300)

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