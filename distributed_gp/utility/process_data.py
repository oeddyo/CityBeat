from event_interface import EventInterface
from event_feature import EventFeature
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from bson.objectid import ObjectId
from corpus import Corpus

import operator
import string
import types
import random
import math

def readCrowdFlowerData2():
	
	# load modified 
	
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	true_events = []
	false_events = []
	
	fid2 = open('labeled_data_cf/modified_event_labels.txt', 'r')
	modified_events = {}
	for line in fid2:
		t = line.split()
		modified_events[str(t[0])] = int(t[1])
	fid2.close()
		
	# put the data into a text file first
	fid = open('labeled_data_cf/data2.txt','r')
	for line in fid:
		if len(line.strip()) == 0:
			continue
		t = line.strip().split()
		if not len(t) == 3:
			continue
		label = t[0].lower()
		confidence = float(t[1])
		event_id = str(t[2].split('/')[-1])
		if label == 'not_sure':
			continue
		if label == 'yes':
			label = 1
		else:
			label = -1
		event = ei.getDocument({'_id':ObjectId(event_id)})
		event['label'] = label
		if modified_events.has_key(event_id):
			event['label'] = modified_events[event_id]
			
		if event['label'] == 0:
			continue
		
		if event['actual_value'] < 8:
			continue
		
		if event['label'] == 1:
			 true_events.append(event)
		else:
			if confidence == 1:
				false_events.append(event)
			
	fid.close()
	return true_events, false_events
	
def readCrowdFlowerData():
	
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	true_events = []
	false_events = []
	
	# put the data into a text file first
	fid = open('labeled_data_cf/data2.txt','r')
	np = 0
	nn = 0
	for line in fid:
		if len(line.strip()) == 0:
			continue
		t = line.split()
		if not len(t) == 3:
			continue
		label = t[0].lower()
		confidence = float(t[1])
		event_id = t[2].split('/')[-1]
		if label == 'yes':
			event = ei.getDocument({'_id':ObjectId(event_id)})
			event['label'] = 1
			true_events.append(event)
		if label == 'no':
			if confidence < 1:
				continue
			event = ei.getDocument({'_id':ObjectId(event_id)})
			event['label'] = -1
			if event['actual_value'] < 8:
				continue
			false_events.append(event)
	fid.close()
	return true_events, false_events

def readFromArff():
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
	return true_events, false_events

def generateData(use_all_event=True):
	
	corpus = Corpus()
	corpus.buildCorpusOnDB('citybeat', 'candidate_event_25by25_merged')
	
#	true_event_list, false_event_list = readCrowdFlowerData()
	true_event_list, false_event_list = readFromArff()
#	true_event_list, false_event_list = readCrowdFlowerData2()
	EventFeature.GenerateArffFileHeader()
	true_events = []
	for event in true_event_list:
		event = EventFeature(event, corpus)
		feature_vector = event.extractFeatures(3)
		true_events.append(feature_vector)
		
	
	false_events = []
	for event in false_event_list:
		event = EventFeature(event, corpus)
		feature_vector = event.extractFeatures(3)
		false_events.append(feature_vector)

	random.shuffle(false_events)
			
	for fv in true_events:
		for i in xrange(0, len(fv) - 1):
			print fv[i],',',
		print fv[-1]
		
	j = 0
	for fv in false_events:
		for i in xrange(0, len(fv) - 1):
			print fv[i],',',
		print fv[-1]
		j += 1
		if not use_all_event and j == len(true_events):
			break

if __name__=='__main__':
	generateData()
	#readFromArff()