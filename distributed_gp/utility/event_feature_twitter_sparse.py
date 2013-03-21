from event_interface import EventInterface
from event_feature import EventFeature
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from corpus import Corpus
from _kl_divergence import kldiv

import kl_divergence as KLDivergence

import sys
import operator
import string
import types
import random
import math

class EventFeatureTwitterSparse(EventFeatureSparse):
	# this class is the extension of class Event, especially for feature extraction
	# to prevent the class Event from being too long to read
	
	def __init__(self, event, corpus=None, representor=None):
		super(EventFeatureSparse, self).__init__(event, corpus, representor)
	
	def getAllWordTFIDF(self):
		index_list, word_list, tfidf_list = self._representor.getTfidfVector(self._event)
		feature_list = []
		for i in xrange(0, len(index_list)):
			feature_list.append([index_list[i], word_list[i], tfidf_list[i]])
		return feature_list
		        
	def printFeatures(self, word_index):
		print '{',
		tfidf_list = self.getAllWordTFIDF()
		sorted_tfidf_list = []
		
		for ind,word,freq in tfidf_list:
			assert word in word_index
			sorted_tfidf_list.append([word_index[word], freq])
			
		sorted_tfidf_list.sort(key=operator.itemgetter(0))
		
		for ind, freq in sorted_tfidf_list:
			print ind, freq,',',
					
		feature_list = self.extractFeatures()
		n = len(feature_list)
		for i in xrange(0, n-1):
			print i+len(word_index), feature_list[i],',',
		print n-1+len(word_index), feature_list[-1],
		print '}'
		
	@staticmethod
	def GenerateArffFileHeader(word_list):
		print '@relation CityBeatEvents'

		for word in word_list:
			print '@attribute tfidf_' + word.encode('utf8') + ' real'
			
		print '@attribute label {1,-1}'
		print '@data'
		
			
if __name__=='__main__':
	generateData()
#	ei = EventInterface()
#	ei.setDB('historic_alarm')
#	ei.setCollection('labeled_event')
#	event = ei.getDocument()
#	e = EventFeature(event)
#	e.getHistoricFeatures()