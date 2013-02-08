from stopwords import Stopwords

import operator


class CaptionParser:
	
	def __init__(self, stopword_removal):
		self._word_dict = {}
		self._document_number = 0  # number of documents accumulated
		self._stopword_removal = stopword_removal
	
	def getTopWords(self, k):
		if len(self._word_dict) == 0:
			return []
		new_top_words = []
		top_words = sorted(self._word_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
		for i in xrange(0, len(top_words)):
			tmp_tuple = (top_words[i][0], 1.0*top_words[i][1] / self._document_number)
			new_top_words.append(tmp_tuple)
		return new_top_words[0:min(k, len(new_top_words))]
	
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
		new_cap = ''
		pre_is_cap = False
		for c in cap:
			if c.isupper():
				if not pre_is_cap:
					new_cap += ' '
				new_cap += c.lower()
				pre_is_cap = True
				continue

			if c.islower():
				new_cap += c
			else:
				new_cap += ' '
			pre_is_cap = False
			 
		words = new_cap.split()
		stopword_list = Stopwords.stopwords()
		tmp_dict = {} 
		
		for word in words:
			word = word.strip()
			if self._stopword_removal and word in stopword_list:
				continue
			if word in tmp_dict.keys():
				tmp_dict[word] = tmp_dict[word] + 1
			else:
				tmp_dict[word] = 1
		return tmp_dict
		
if __name__ == '__main__':
	cp = CaptionParser(True)
	cap1 = '@ToutFuckYou  ###noGood   GOD love  bad  guys. ! I hate you.'
	cap2 = '@ToutFuckYou  ###badminton   GOD love  bad  guys. ! I hate you.'
	print cp._preprocessCaption(cap2)