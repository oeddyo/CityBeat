import operator

class CaptionParser:
	
	def __init__(self):
		self._word_dict = {}
		self._document_number = 0  # number of documents accumulated
	
	def getTopWords(self, k):
		if len(self._word_dict) == 0:
			return []
		top_words = sorted(self._word_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
		for i in xrange(0, len(top_words)):
			tmp_tuple = (top_words[i][0], 1.0*top_words[i][1] / self._document_number)
			top_words[i] = tmp_tuple
		return top_words[0:min(k, len(top_words))]
	
	def insertCaption(self, cap):
		if cap is None or len(cap) == 0:
			return
		self._document_number = self._document_number + 1
		tmp_dict = self._preprocessCaption(cap)
		for word in tmp_dict.keys():
			if word in self._word_dict.keys():
				self._word_dict[word] = self._word_dict[word] + 1
			else:
				self._word_dict[word] = 1
	
	def _preprocessCaption(self, cap):
		tmp_dict = {}
		words = cap.lower().split(' ')
		for word in words:
			new_word = self._extractWord(word)
			if len(new_word) == 0:
				continue
			if new_word in tmp_dict.keys():
				tmp_dict[new_word] = tmp_dict[new_word] + 1
			else:
				tmp_dict[new_word] = 1
		return tmp_dict
	
	def _extractWord(self, word):
		new_word = ''
		for c in word:
			if c>='a' and c<='z':
				new_word = new_word + c
		return new_word