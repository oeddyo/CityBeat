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

def main():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	events = ei.getAllDocuments()
	
	fid2 = open('labeled_data_cf/true_label2.txt', 'r')
		
	labels = {}
	
	for line in fid2:
		t = line.split(',')
		labels[str(t[0])] = int(t[1])
	fid2.close()
	
	pos = 0
	tot = 0
	for event in events:
		region = event['region']
		id = str(event['_id'])
		if id not in labels.keys():
			continue
		
		tot += 1
		if (region['min_lat'] == 40.75419436 and region['max_lat'] == 40.75949964 and
		   region['min_lng'] == -73.98609448 and region['max_lng'] == -73.9780882):
			if labels[id] == 1:
				pos += 1
				print 'pos'
	print pos
	print tot

if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	