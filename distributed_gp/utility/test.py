from event_interface import EventInterface
from event_feature import EventFeature
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from bson.objectid import ObjectId

import operator
import string
import types
import random
import math


unique_id = set()
photo_n = 0
event_n = 0


ei = EventInterface()
ei.setDB('citybeat')
ei.setCollection('candidate_event_25by25')

events = ei.getAllDocuments()
for event in events:
	e = Event(event)
	if event['actual_value'] < 10:
		continue
	photos = event['photos']
	photo_n += len(photos)
	event_n += 1
	for photo in photos:
		unique_id.add(photo['id'])

print photo_n
print event_n
print photo_n*1.0/event_n
print len(unique_id)


