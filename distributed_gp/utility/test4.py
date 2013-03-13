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
	ei.setCollection('next_week_candidate_event_25by25_merged')
	event_cur = ei.getAllDocuments()
	event_list = []
	for event in event_cur:
		event_list.append(event)
	random.shuffle(event_list)
	for event in event_list[0:200]:
		print event['id']


if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	