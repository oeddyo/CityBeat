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
	fid1 = open('labeled_data_cf/balanced_data_with_true_label.txt', 'r')
	fid2 = open('labeled_data_cf/modified_event_labels.txt', 'r')
	true_events = []
	false_events = []
	
	modified_events = {}
	for line in fid2:
		t = line.split()
		modified_events[str(t[0])] = int(t[1])
	
	for line in fid1:
		t = line.split(',')
		ID = str(t[0])
		label = int(t[1])
		print ID+','+str(label)
	
	fid1.close()
	fid2.close()
		
def main():
	writeFile()
	
	
if __name__=='__main__':
	main()

