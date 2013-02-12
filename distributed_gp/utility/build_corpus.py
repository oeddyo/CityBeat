from photo_interface import PhotoInterface
from caption_parser import CaptionParser
from mongodb_interface import MongoDBInterface
from photo import Photo

import random


if __name__ == '__main__':
	mi = MongoDBInterface()
	mi.setDB('test_caption')
	mi.setCollection('captions')
	
	cp = CaptionParser(True)
	
	i = 0
	captions = mi.getAllDocuments()
	for caption in captions:
		i += 1
		if i % 1000 == 0:
#			print cp.getTopWords(200)
			print i
			print len(cp._)
		cp.insertCaption(caption['caption'])

	for word, value in cp.getTopWords(300):
		print '\''+word+'\',',
	print