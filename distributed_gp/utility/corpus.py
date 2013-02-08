from event_interface import EventInterface
from caption_parser import CaptionParser
from photo import Photo

import time
import math
import operator

class Corpus(object):
	
	def __init__(self):
		self._corpus_df = {}
		
	def _addDocument(self, word_list):
		for word, value in word_list:
			if word in self._corpus_df:
				self._corpus_df[word] += 1
			else:
				self._corpus_df[word] = 1
	
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
		for i in xrange(0, len(word_list)):
			word = word_list[i][0]
			tf = word_list[i][1]
			tfidf = - tf * math.log(self._corpus_df[word] + 1)
			word_list[i]= (word, tfidf)
		word_list.sort(key=operator.itemgetter(1), reverse=True)
		return word_list[0:min(k, len(word_list))]
			
	
if __name__ == '__main__':
	pass