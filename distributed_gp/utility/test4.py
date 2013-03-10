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
	my_region = {'min_lat': 40.75419436, 'max_lng': -73.9780882, 'min_lng': -73.98609448, 'max_lat': 40.75949964}
	pi = PhotoInterface()
	pi.setDB('citybeat')
	pi.setCollection('photos')
	photos1 = pi.rangeQuery(my_region, ['1354319474', '1354320288'])
	pi.setCollection('photos_no_duplicate')
	photos2 = pi.rangeQuery(my_region, ['1354319474', '1354320288'])
	
	print photos1.count()
	print photos2.count()
	
	dict1 = {}
	for photo in photos1:
		dict1[photo['id']] = 1
	
	print len(dict1)
	
	dict2 = {}
	for photo in photos2:
		dict2[photo['id']] = 1
	
	print len(dict2)


if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	