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


def writeFile():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	fid1 = open('labeled_data_cf/balanced_data_Res.arff', 'r')
	fid2 = open('labeled_data_cf/modified_event_labels.txt', 'r')
	true_events = []
	false_events = []
	
	modified_events = {}
	for line in fid2:
		t = line.split()
		modified_events[str(t[0])] = int(t[1])
	
	for line in fid1:
		t = line.split(',')
		ID = str(t[13])
		label = int(t[15])
		event = ei.getDocument({'_id':ObjectId(ID)})
		event['label'] = label
		if modified_events.has_key(ID):
			event['label'] = modified_events[ID]
		
		if event['actual_value'] < 8:
			continue
		
		if event['label'] == -1:
			false_events.append(event)
		else:
			if event['label'] == 1:
				true_events.append(event)
	
	fid1.close()
	fid2.close()
	
	for event in true_events + false_events:
		print str(event['_id'])+','+str(event['label'])
		
def main():
	writeFile()
	
	
if __name__=='__main__':
	main()

