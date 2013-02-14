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

ei = EventInterface()
ei.setDB('citybeat')
ei.setCollection('candidate_event_25by25_merged')

#51148f4fc2a3754cfe66a178

event =ei.getDocument({'_id':ObjectId('51148f4fc2a3754cfe66a178')})

cp = CaptionParser(True)

for photo in event['photos']:
	p = Photo(photo)
	print p.getCaption()
