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

import operator
import string
import types
import random
import math

class EventFeatureSparse(EventFeature):
	# this class is the extension of class Event, especially for feature extraction
	# to prevent the class Event from being too long to read
	
	def __init__(self, event, corpus=None, representor=None, corpus_len=0):
		super(EventFeatureSparse, self).__init__(event, corpus, representor)
		self._corpus_len = corpus_len
	
	def getAllWordTFIDF(self):
		index_list, word_list, tfidf_list = self._representor.getTfidfVector(self._event)
		feature_list = []
		for i in xrange(0, len(index_list)):
			feature_list.append([index_list[i], word_list[i], tfidf_list[i]])
		return feature_list
		        
	def printFeatures(self):
		print '{',
		tfidf_list = self.getAllWordTFIDF()
		if len(tfidf_list) > 0:
			for ind,word,freq in tfidf_list:
					print ind, freq,',',
					
		feature_list = self.extractFeatures()
		n = len(feature_list)
		for i in xrange(0, n-1):
			print i+self._corpus_len, feature_list[i],',',
		print n-1+self._corpus_len, feature_list[-1],
		print '}'
		
#	@staticmethod
	def GenerateArffFileHeader(self):
		print '@relation CityBeatEvents'
		
		word_list = self._representor.getCorpusWordsVector()
		for word in word_list:
			print '@attribute tfidf_' + word + ' real'
			
		print '@attribute AvgCaptionLen real'
		print '@attribute AvgPhotoDis real'
		print '@attribute AvgPhotoDisbyCap real'
		print '@attribute CaptionPercentage real'
#		print '@attribute PeopleNumber real'
#		print '@attribute Duration real'
#		print '@attribute PercentageOfStopwordsFromTopWords real'
		print '@attribute PredictedStd real'
		print '@attribute TopWordPopularity real'
		print '@attribute Zscore real'
		print '@attribute Entropy real'
		print '@attribute TheRatioOfPeopleToPhoto real'
#		print '@attribute diff_AvgPhotoDis real'
#		print '@attribute diff_TopWordPopularity real'
#		print '@attribute diff_Entropy real'

		print '@attribute tfidf1 real'	
		print '@attribute tfidf2 real'	
		print '@attribute tfidf3 real'
		
		print '@attribute NumberOfHashtages1 real'	
		print '@attribute NumberOfHashtages2 real'	
		print '@attribute NumberOfHashtages3 real'	
		
		print '@attribute NumberOfPhotsoContaingTopWord1 real'
		print '@attribute NumberOfPhotsoContaingTopWord2 real'
		print '@attribute NumberOfPhotsoContaingTopWord3 real'
		
		print '@attribute Top10PhotoLocationNameFreq real'
		print '@attribute Top3PhotoLocationNameSame real'
		
		print '@attribute ID string'
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