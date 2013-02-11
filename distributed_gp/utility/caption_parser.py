from stopwords import Stopwords

import operator


class CaptionParser:
	
	def __init__(self, stopword_removal):
		self._word_dict = {}
		self._document_number = 0  # number of documents accumulated
		self._stopword_removal = stopword_removal
	
	def getTopWords(self, k, percentage=True):
		# if not percentage, it returns the number of photos containing that word.
		if len(self._word_dict) == 0:
			return []
		new_top_words = []
		top_words = sorted(self._word_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
		for i in xrange(0, len(top_words)):
			if percentage:
				value = 1.0*top_words[i][1] / self._document_number
			else:
				value = top_words[i][1]
			tmp_tuple = (top_words[i][0], value)
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
		def removeAt(cap):
			# remove @eddie
			end_at = [' ', '\t', '#']
			new_cap = ''
			pre_is_at = False
			for c in cap:
				if c =='@':
					pre_is_at = True
					continue
				
				if pre_is_at == True:
					if c in end_at:
						pre_is_at = False
				
				if pre_is_at == False:
					new_cap += c
			
			return new_cap
			
		cap = removeAt(cap)
			
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
	cap1 = 'gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb'
	print cp._preprocessCaption(cap1)