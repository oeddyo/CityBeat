from event_interface import EventInterface


ei = EventInterface()
ei.setDB('citybeat')
ei.setCollection('candidate_event_25by25_merged')

ei2 = EventInterface()
ei2.setDB('AmazonMT')
ei2.setCollection('candidate_event_25by25_merged')

events = ei.getAllDocuments()
for event in events:
	ei2.saveDocument(event)