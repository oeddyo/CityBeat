from event_interface import EventInterface
from event_feature import EventFeature
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from corpus import Corpus

import operator
import string
import types
import random
import math

class EventFrontend(EventFeature):
	# this class is only for providing data to jerry's front end
	
	def __init__(self, event, corpus):
		super(EventFrontend, self).__init__(event)
		self._corpus = corpus
				
	def _getTopKeywordsWithoutStopwords(self, k):
		# this method will return topwords without stopwords
		return self._getTopWords(k, stopword_removal=True)
		
	def _getRandomPhotosAssociatedWithKeywords(self, top_keywords, k=10):
		# get photos associated with the top_keywords
		# k specifies the number of photos to show
		res = []
		for (word, fre) in top_keywords:
			photos = self.getPhotosbyKeyword(word)
			random.shuffle(photos)
			k = min(len(photos), k)
			# discard the keywords with only one photo
			if k == 1:
				break
			res.append([word, fre, photos[0:k]])
		return res
	
	def getTopKeywordsAndPhotos(self, num_keywords, num_photos):
		keywords = self._getTopKeywordsWithoutStopwords(num_keywords)
		return self._getRandomPhotosAssociatedWithKeywords(keywords, num_photos)
	
	def getTopKeywordsAndPhotosByTFIDF(self, num_keywords, num_photos):
		keywords = self._getTopKeywordsWithoutStopwords(100000)
		keywords = self._corpus.chooseTopWordWithHighestTDIDF(keywords, num_keywords)
		return self._getRandomPhotosAssociatedWithKeywords(keywords, num_photos)
			
if __name__=='__main__':
	
	collection = 'candidate_event_10by10_merged'
	
	c = Corpus()
	c.buildCorpusOnDB('citybeat', collection)
	
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection(collection)
	events = ei.getAllDocuments()
	for event in events:
		event = EventFrontend(event, c)
		print event.getTopKeywordsAndPhotosByTFIDF(10,0)
