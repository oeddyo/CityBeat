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
	fid1 = open('arff\mod1.arff')
	fid2 = open('arff\mod2.arff')
	
	dict2 = {}
	for line in fid2:
		tup = line.strip().split(',')
		dict2[tup[0]] = tup[1]
	
	for line in fid1:
		tup = line.strip().split(',')
		if tup[0] not in dict2.keys() or dict2[tup[0]]!=tup[1]:
			print tup[0]
	
	
	


if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	