from event_interface import EventInterface
from event_feature import EventFeature
from event_feature_sparse import EventFeatureSparse
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from bson.objectid import ObjectId
from corpus import Corpus
from representor import Representor

import operator
import string
import types
import random
import math

import sys

def loadNextWeekData():
	
	# load modified 
	
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('next_week_candidate_event_25by25_merged')
	
	true_events = []
	false_events = []
	
	fid2 = open('labeled_data_cf/label_next_week.txt', 'r')
	
	for line in fid2:
		t = line.split(',')
		id = str(t[0])
		label = int(t[1])
		
		event = ei.getDocument({'_id':ObjectId(id)})
		event['label'] = label
		e = Event(event)
		if e.getActualValue() < 8 or event['label'] == 0:
#			print 'bad event ' + id
			continue
		if event['label'] == 1:
			true_events.append(event)
		else:
			false_events.append(event)
			
	fid2.close()
	return true_events, false_events

def generateData():
	corpus = Corpus()
	corpus.buildCorpusOnDB('citybeat', 'next_week_candidate_event_25by25_merged')
	true_event_list, false_event_list = loadNextWeekData()
	EventFeature(None).GenerateArffFileHeader()
		
	for event in true_event_list + false_event_list:
		EventFeature(event, corpus).printFeatures()

		
def main():
	generateData()

if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	
	
	
	
	
	
#def loadRawLabeledData():
#	
#	ei = EventInterface()
#	ei.setDB('citybeat')
#	ei.setCollection('candidate_event_25by25_merged')
#	
#	true_events = []
#	false_events = []
#	
#	# put the data into a text file first
#	fid = open('labeled_data_cf/data2.txt','r')
#	np = 0
#	nn = 0
#	for line in fid:
#		if len(line.strip()) == 0:
#			continue
#		t = line.split()
#		if not len(t) == 3:
#			continue
#		label = t[0].lower()
#		confidence = float(t[1])
#		event_id = t[2].split('/')[-1]
#		if label == 'yes':
#			event = ei.getDocument({'_id':ObjectId(event_id)})
#			event['label'] = 1
#			true_events.append(event)
#		if label == 'no':
#			if confidence < 1:
#				continue
#			event = ei.getDocument({'_id':ObjectId(event_id)})
#			event['label'] = -1
#			if event['actual_value'] < 8:
#				continue
#			false_events.append(event)
#	fid.close()
#	return true_events, false_events
