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


def main():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	events = ei.getAllDocuments()
	
	ti = TweetInterface()
	zero = 0
	for event in events:
		tweet_cluster = TweetCluster()
		tweet_cluster.setRegion(event['region'])
		e = EventFeature(event)
		tweet_cluster.setPeriod([e.getEarliestPhotoTime(), e.getLatestPhotoTime()])
		tweet_cluster.getTweetFromRangeQuery()
		nt = tweet_cluster.getNumberOfTweets()
		if nt == 0:
			zero += 1
			print e.getDuration(),  time.gmtime(e.getEarliestPhotoTime())
	print zero
	
	


if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	