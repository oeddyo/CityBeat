from event_interface import EventInterface
from caption_parser import CaptionParser
from photo import Photo

import time
import math
import operator

class Corpus(object):
	
	def __init__(self, leastDF=5):
		self._corpus_df = {}
		self._corpus_n = 0
		self._leastDF = leastDF
		
	def _addDocument(self, word_list):
		for word, value in word_list:
			if word in self._corpus_df:
				self._corpus_df[word] += 1
			else:
				self._corpus_df[word] = 1
		self._corpus_n += 1
	
	def getWordList(self, event):
		# word_list is a list of (word, freq)
		cp = CaptionParser(True)
		for photo in event['photos']:
			photo = Photo(photo)
			cp.insertCaption(photo.getCaption())
		return cp.getTopWords(100000, False)
	
	def buildCorpusOnDB(self, db, collection):
		ei = EventInterface()
		ei.setDB(db)
		ei.setCollection(collection)
		events = ei.getAllDocuments()
		for event in events:
			word_list = self.getWordList(event)
			self._addDocument(word_list)
			
	def chooseTopWordWithHighestTDIDF(self, word_list, k=10):
		# word_list is a list of (word, freq)
		new_word_list = []
		for i in xrange(0, len(word_list)):
			word = word_list[i][0]
			tf = word_list[i][1]
			# note that the corpus must be consistent with the events
			# that means, we cannot use the corpus built from 15by15 for 10by10
			if self._corpus_df[word] >= self._leastDF:
				tfidf = tf * math.log(self._corpus_n * 1.0 / self._corpus_df[word])
				new_word_list.append((word, tfidf))
		new_word_list.sort(key=operator.itemgetter(1), reverse=True)
		return new_word_list[0:min(k, len(new_word_list))]
			
	
if __name__ == '__main__':
	pass