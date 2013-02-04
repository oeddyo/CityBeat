from event_interface import EventInterface
from bson.objectid import ObjectId
from event_feature import EventFeature


ei = EventInterface()
ei.setDB('historic_alarm')
ei.setCollection('raw_event')


ei2 = EventInterface()
ei2.setDB('historic_alarm')
ei2.setCollection('labeled_event')


#fid = open('final_labels.txt', 'r')
#
#for line in fid:
#	vals = line.split()
#	label = -1
#	if len(vals) > 1 and vals[1] == '1':
#		label = 1
#	event = ei.getDocument({'_id':ObjectId(vals[0])})
#	event['label'] = label
#	ei2.updateDocument(event)

events = ei2.getAllDocuments()
for event in events:
	label = event['label']
	event = EventFeature(event)
	(lat, lng) = event._getPhotoAvgLocation()
	print lat, lng, label