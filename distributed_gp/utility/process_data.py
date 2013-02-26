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



def getCorpusWordList(rep, event_list):
	word_index={}
	word_list=[]
	ind = 0
	for event in event_list:
		e = EventFeatureSparse(event, representor=rep)
		wl = e.getAllWordTFIDF()
		for i in xrange(0, len(wl)):
			word = wl[i][1]
			if word not in word_index:
				word_index[word] = ind
				ind += 1
				word_list.append(word)
	return word_index, word_list

def generateData(use_all_event=True):
	
	rep = Representor()
#	rep = None
	corpus = Corpus()
	corpus.buildCorpusOnDB('citybeat', 'candidate_event_25by25_merged')
	
#	true_event_list, false_event_list = readCrowdFlowerData()
#	true_event_list, false_event_list = readFromArff()
#	true_event_list, false_event_list = readCrowdFlowerData2()
	if use_all_event:
		true_event_list, false_event_list = readCrowdFlowerData2()
	else:
		true_event_list, false_event_list = readFromArff()
	
	word_index, word_list = getCorpusWordList(rep, true_event_list + false_event_list)
	EventFeatureSparse(None).GenerateArffFileHeader(word_list)

	for event in true_event_list:
		EventFeatureSparse(event, corpus, rep).printFeatures(word_index)
		
	random.shuffle(false_event_list)
	j = 0
	for event in false_event_list:
		EventFeatureSparse(event, corpus, rep).printFeatures(word_index)
		j += 1
		if not use_all_event and j == len(true_events):
			break

def main():
	
	if len(sys.argv) > 1 and sys.argv[1] == 'unbalanced':
		generateData()
	else:
		assert sys.argv[1] == 'balanced'
		generateData(False)

if __name__=='__main__':
	main()