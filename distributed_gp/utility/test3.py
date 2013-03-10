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

def loadUnbalancedData():

	
	true_events = []
	false_events = []
	
	fid2 = open('labeled_data_cf/true_label2.txt', 'r')
	
	true_event_list = []
	false_event_list = []
		
	for line in fid2:
		t = line.split(',')
		id = str(t[0])
		label = int(t[1])
		if label == 0:
			continue
		if label == 1:
			true_event_list.append(id)
		else:
			false_event_list.append(id)
	fid2.close()
	
	random.shuffle(true_event_list)
	random.shuffle(false_event_list)
	
	mixed_event_list = true_event_list[0:25] + false_event_list[0:25]
	random.shuffle(mixed_event_list)
	
	for id in mixed_event_list:
		print id

	
	return true_events, false_events


if __name__=='__main__':
	loadUnbalancedData()
	
	
	
	
	
	
	
	