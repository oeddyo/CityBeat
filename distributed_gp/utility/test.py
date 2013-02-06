from event_interface import EventInterface

from prediction_interface import PredictionInterface

from region import Region

from bson.objectid import ObjectId
from event import Event
from event_feature import EventFeature

from datetime import datetime


ei = EventInterface()

ei.setCollection('candidate_event_10by10')

events = ei.getAllDocuments()

i = 0
for event in events:
	if len(event['photos']) < 8:
		continue
	i += 1
	event = EventFeature(event)
	cor = event._getPhotoAvgLocation()
	print cor[0], cor[1]