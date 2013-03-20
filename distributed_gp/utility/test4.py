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


import operator
import string
import types
import random
import math

import sys


def main():
	ei = EventInterface()
	ei.setCollection('candidate_event_25by25_merged')
	event_cur = ei.getAllDocuments()
#	for event in event_cur:
#		print event['created_time']
	
	ti = TweetInterface()
	tweet_cur = ti.getAllDocuments()
	i = 0
	for tweet in tweet_cur:
		i += 1
		if i % 10 == 0:
			print Tweet(tweet).getCreatedUTCTimestamp()
	
	
	


if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	