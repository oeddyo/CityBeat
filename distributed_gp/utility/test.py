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


		
def main():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	event = ei.getEventByID('511486b7c2a3754cfe6694e2')
	
	e = Event(event)
	
	print len(event['photos'])
	print e._getActualValueByCounting()
	e.selectOnePhotoForOneUser()
	ee = e.toJSON()
	print len(ee['photos'])
	
	
if __name__=='__main__':
	main()

