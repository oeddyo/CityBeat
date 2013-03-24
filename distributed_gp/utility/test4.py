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
	print pc.count()
	
	ids = set()
	for photo in pc:
		ids.add(photo['id'])

	print len(ids)
	print pi2.rangeQuery(region, [st, et]).count()


if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	