from photo_interface import PhotoInterface
from caption_parser import CaptionParser
from photo import Photo
from mongodb_interface import MongoDBInterface

import random


if __name__ == '__main__':
	pi = PhotoInterface()
	pi.setDB('citybeat')
	pi.setCollection('photos')
	
	mi = MongoDBInterface()
	mi.setDB('test_caption')
	mi.setCollection('captions')
	
	photos = pi.getAllDocuments()
	for photo in photos:
		i = random.randint(0,10)
		if i > 0:
			continue
		p = Photo(photo)
		cap = p.getCaption()
		if len(cap) > 0:
			cap = {'caption':cap}
			mi.saveDocument(cap)