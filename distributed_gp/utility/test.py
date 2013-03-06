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

def generateTrueLabelFile():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	events = {}
	fid1 = open('labeled_data_cf/true_label.txt', 'r')
	true_events = []
	false_events = []
	unknown_events = []
	
	for line in fid1:
		t = line.split(',')
		id = str(t[0])
		label = int(t[1])
		events[id] = label
		
	fid1.close()
	
	for id, label in events.items():
		event = ei.getDocument({'_id':ObjectId(id)})
		event['label'] = label
		e = Event(event)
		if e.getActualValue() < 8:
#			print 'bad event ' + id
			continue
		if event['label'] == -1:
			false_events.append(event)
		else:
			if event['label'] == 1:
				true_events.append(event)
			else:
				unknown_events.append(event)
	
	
	for event in true_events + false_events + unknown_events:
		print str(event['_id'])+','+str(event['label'])
	
if __name__=='__main__':
	generateTrueLabelFile()

