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
from tweet_interface import TweetInterface
from tweet import Tweet
from tweet_cluster import TweetCluster


import operator
import string
import types
import random
import math
import time

import sys


def getClassifiedLabels():
	fid = open('results/181_logistic_regression_result.txt')
	
	tp = []
	tn = []
	fp = []
	fn = []
	for line in fid:
		vals = line.strip().split(',')
		id = vals[0]
		predicted_label = int(vals[1])
		true_label = int(vals[2])
		if predicted_label == true_label:
			if true_label == 1:
				tp.append(id)
			else:
				tn.append(id)
		else:
			if predicted_label < true_label:
				fn.append(id)
			else:
				fp.append(id)
	
	for id in fn:
		print id
		
#	print len(tp)
#	print len(tn)
#	print len(fp)
#	print len(fn)			
#		
	
	fid.close()

def getBaselineEvents():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('baseline_candidate_events')
	
	events = ei.getAllDocuments()
	
	event_list = []
	
	for event in events:
		e = Event(event)
		if e.getActualValue() < 8 or e.getZscore() < 3:
			continue
		event_list.append(event)
	
#	print len(event_list)
	
#	return 
	
	random.shuffle(event_list)
	
	for i in xrange(50):
		print event_list[i]['_id']	

def mergeBaselineEvents():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('baseline_candidate_events')
	
	ei2 = EventInterface()
	ei2.setDB('citybeat')
	ei2.setCollection('baseline_candidate_events_merged')
	
	events = ei.getAllDocuments()
	
	for event in events:
		ei2.addEvent(event)

def main():
	pi = PhotoInterface()
	pi.setDB('citybeat')
	pi.setCollection('photos')
	
	pi2 = PhotoInterface()
	pi2.setDB('citybeat')
	pi2.setCollection('photos_no_duplicate')
	
	region = {}
	region['min_lat'] = 40.690531
	region['min_lng'] = -74.058151
	region['max_lat'] = 40.823163
	region['max_lng'] = -73.857994
	st = '1352937600'
	et = '1355615999'
	pc = pi.rangeQuery(region, [st, et])
#	print pc.count()
	
	ids = set()
	for photo in pc:
		ids.add(photo['link'])

	print len(ids)
	print pi2.rangeQuery(region, [st, et]).count()

def generateUnlabeledEvent():
	ids = []
	fid = open('labeled_data_cf/all_data.txt')
	for line in fid:
		vals = line.strip().split()
		label = vals[0]
		conf = float(vals[1])
		id = vals[2].split('/')[-1]
		if label.lower() != 'yes' and conf < 1:
			ids.append(id)
	random.shuffle(ids)
	for i in xrange(50):
		print ids[i]
	fid.close()
	
def getCaptionStatistics():
	pi = PhotoInterface()
	pi.setDB('citybeat')
	pi.setCollection('photos_no_duplicate')
	tot = 0
	withCap = 0
	l = 0
	for photo in pi.getAllDocuments():
		cap = Photo(photo).getCaption()
		tot += 1
		if len(cap) == 0:
			continue
		withCap += 1
		l += len(cap)
	
	print 1.0*withCap / tot
	print 1.0*l / withCap
	

if __name__=='__main__':
#	getClassifiedLabels()
#	mergeBaselineEvents()
#	generateUnlabeledEvent()
	getCaptionStatistics()
	
	
	
	
	
	
	