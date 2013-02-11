from event_interface import EventInterface

from prediction_interface import PredictionInterface

from region import Region

from bson.objectid import ObjectId
from event import Event

from datetime import datetime
import random

n = 300
ei = EventInterface()
ei.setCollection('candidate_event_10by10_merged')
events = ei.getAllDocuments()
event_list = []

for event in events:
	event_list.append(event)

random.shuffle(event_list)


ei2 = EventInterface()
ei2.setDB('label')
ei2.setCollection('label_10by10')

i = 0
for event in event_list:
	ei2.saveDocument(event)
	i += 1
	if i == 300:
		break