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


#def floatEqual(f1, f2):
#	return abs(f1 - f2) <= 1e-8
#
#def main():
#	pi = PhotoInterface()
#	pi.setDB('citybeat')
#	pi.setCollection('photos_no_duplicate')
#	photos = pi.getAllDocuments()
#	l = 0
#	c = 0
#	i = 0
#	for photo in photos:
#		i += 1
#		if i == 50000:
#			break
#		try:
#			cap = photo['caption']['text']
#			if len(cap) > 0:
#				l += len(cap)
#				c += 1
#		except Exception as e:
#			pass
#	print l * 1.0 / c


	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	events = ei.getAllDocuments()
	
	
	event = ei.getEventByID('511478c8c2a3754cfe6684a9')
	print event['region']
		
	lat = (event['region']['min_lat'] + event['region']['max_lat'])/2
	lon = (event['region']['min_lng'] + event['region']['max_lng'])/2
	fid1 = open('region_cache/25_25.txt', 'r')
	for line in fid1:
		cor = line.split(' ')
		for i in xrange(len(cor)):
			cor[i] = float(cor[i])
		if float(cor[0]) <= lat and lat <= float(cor[2]) and float(cor[1]) <= lon and lon <= float(cor[3]):
			min_lat = cor[0]
			max_lat = cor[2]
			min_lng = cor[1]
			max_lng = cor[3]
			print min_lat, max_lat, min_lng, max_lng
			break
	fid1.close()
	
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
		
		if (floatEqual(region['min_lat'], min_lat) and floatEqual(region['max_lat'], max_lat)
		   and floatEqual(region['min_lng'], min_lng) and floatEqual(region['max_lng'], max_lng)):
		  tot += 1
		  if labels[id] == 1:
		  	pos += 1
		  	print id
	print pos
	print tot

if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	