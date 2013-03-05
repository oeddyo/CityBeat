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

def insertEvents():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	ei2 = EventInterface()
	ei2.setDB('citybeat')
	ei2.setCollection('online_candidate')
	
	ids = ['51148288c2a3754cfe668edd', '51147952c2a3754cfe6684ee',
	       '51148a7ec2a3754cfe669977', '51147967c2a3754cfe668503']
	
	for id in ids:
		event = ei.getDocument({'_id':ObjectId(id)})
		ei.addEvent(event)	
	
if __name__=='__main__':
	insertEvents()

