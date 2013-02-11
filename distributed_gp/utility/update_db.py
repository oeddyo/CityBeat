from event_interface import EventInterface

from prediction_interface import PredictionInterface

from region import Region

from bson.objectid import ObjectId
from event import Event

from datetime import datetime
		
		
my_collections = ['candidate_event_10by10', 'candidate_event_15by15',
                  'candidate_event_20by20', 'candidate_event_25by25',
                  'candidate_event_10by10_merged', 'candidate_event_15by15_merged',
                  'candidate_event_20by20_merged', 'candidate_event_25by25_merged',]
               

ei = EventInterface()
for collection in my_collections:
	ei.setCollection(collection)
	print collection
	i = 0
	events = ei.getAllDocuments()
	for event in events:
		e = Event(event)
		av = e.getActualValueByCounting()
		if av != e.getActualValue():
			e.setActualValue(av)
			ei.updateDocument(e)
			i += 1
	print i
               
               