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
from event_feature_twitter import EventFeatureTwitter

import operator
import string
import types
import random
import math

import sys

def loadUnbalancedData(dataEdition):
	
	# load modified 
	
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	true_events = []
	false_events = []
	
	if dataEdition == 'old':
		fid2 = open('labeled_data_cf/true_label3_xia.txt', 'r')
	else:
		fid2 = open('labeled_data_cf/correct_label_3_21.txt', 'r')
		
	modified_events = {}
	
	for line in fid2:
		t = line.split(',')
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
		
		e = Event(event)
		if e.getActualValue() < 8 or event['label'] == 0:
#			print 'bad event ' + id
			continue
		if event['label'] == 1:
			true_events.append(event)
		else:
			if event['label'] == -1 and confidence == 1:
				false_events.append(event)
			
	fid.close()
	return true_events, false_events
	
def loadBalancedData(dataEdition):
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	if dataEdition == 'old':
		fid1 = open('labeled_data_cf/true_label3_xia.txt', 'r')
	else:
		fid1 = open('labeled_data_cf/true_label2.txt', 'r')
		
	true_events = []
	false_events = []
	
	for line in fid1:
		t = line.split(',')
		ID = str(t[0])
		label = int(t[1])
		event = ei.getDocument({'_id':ObjectId(ID)})
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
	
	fid1.close()
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

def generateData(use_all_event=False, sparse=False, dataEdition='new'):
	rep = Representor()
#	rep = None
	corpus = Corpus()
	corpus.buildCorpusOnDB('citybeat', 'candidate_event_25by25_merged')
	
#	true_event_list, false_event_list = loadRawLabeledData()
#	true_event_list, false_event_list = loadBalancedData()
#	true_event_list, false_event_list = loadUnbalancedData()
	if use_all_event:
		true_event_list, false_event_list = loadUnbalancedData(dataEdition)
	else:
		true_event_list, false_event_list = loadBalancedData(dataEdition)
	
	if sparse:
		word_index, word_list = getCorpusWordList(rep, true_event_list + false_event_list)
		EventFeatureSparse(None).GenerateArffFileHeader(word_list)
	else:
		EventFeature(None).GenerateArffFileHeader()
		
	for event in true_event_list:
		if not sparse:
			EventFeature(event, corpus, rep).printFeatures()
		else:
			EventFeatureSparse(event, corpus, rep).printFeatures(word_index)
		
	random.shuffle(false_event_list)
	
	for event in false_event_list:
		if not sparse:
			EventFeature(event, corpus, rep).printFeatures()
		else:
			EventFeatureSparse(event, corpus, rep).printFeatures(word_index)
		

def generateData2(use_all_event=False, sparse=False, dataEdition='new'):
	rep = Representor()
#	rep = None
	corpus = Corpus()
	corpus.buildCorpusOnDB('citybeat', 'candidate_event_25by25_merged')
	
#	true_event_list, false_event_list = loadRawLabeledData()
#	true_event_list, false_event_list = loadBalancedData()
#	true_event_list, false_event_list = loadUnbalancedData()
	if use_all_event:
		true_event_list, false_event_list = loadUnbalancedData(dataEdition)
	else:
		true_event_list, false_event_list = loadBalancedData(dataEdition)
	
	if sparse:
		word_index, word_list = getCorpusWordList(rep, true_event_list + false_event_list)
		EventFeatureSparse(None).GenerateArffFileHeader(word_list)
	else:
		EventFeatureTwitter(None).GenerateArffFileHeader()
		
	for event in true_event_list:
		if not sparse:
			EventFeatureTwitter(event, corpus, rep).printFeatures()
		else:
			EventFeatureSparse(event, corpus, rep).printFeatures(word_index)
		
	random.shuffle(false_event_list)
	
	for event in false_event_list:
		if not sparse:
			EventFeatureTwitter(event, corpus, rep).printFeatures()
		else:
			EventFeatureSparse(event, corpus, rep).printFeatures(word_index)

def main():
	assert len(sys.argv) == 3
	assert sys.argv[1] == 'balanced' or sys.argv[1] == 'unbalanced'
	assert sys.argv[2] == 'old' or sys.argv[2] == 'new'
#	assert sys.argv[2] == 'unsparse' or sys.argv[2] == 'sparse'
	
	balanced = sys.argv[1] == 'balanced'
	dataEdition = sys.argv[2]
	sparse = False
#	sparse = sys.argv[2] == 'sparse'
	generateData2(not balanced, sparse, dataEdition)

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
