


from event_interface import EventInterface
from event import Event


ei = EventInterface()
ei.setCollection('candidate_event_10by10_merged')

ec = ei.getAllDocuments()
print ec
for e in ec:
    print e


