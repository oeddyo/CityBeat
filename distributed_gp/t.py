from utility.event_interface import EventInterface

ei = EventInterface()
ei.setDB('citybeat')
ei.setCollection('baseline_candidate_events')
p = ei.getPhotoDistributionArray()
print p
