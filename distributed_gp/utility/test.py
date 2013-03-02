from event_interface import EventInterface
from event_feature import EventFeature
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from bson.objectid import ObjectId

import operator
import string
import types
import random
import math


		
def main():
	ei = EventInterface()
	ei.setDB('citybeat')
	ei.setCollection('candidate_event_25by25_merged')
	
	ei2 = EventInterface()
	ei2.setDB('citybeat')
	ei2.setCollection('online_candidate')
	ids = ['51148288c2a3754cfe668edd', '51147952c2a3754cfe6684ee', '51148d89c2a3754cfe669eb4', '51147967c2a3754cfe668503']
	ids += ['51147b20c2a3754cfe668697', '51148a7ec2a3754cfe669977', '51147ad8c2a3754cfe668670', '51148ba7c2a3754cfe669b75']

#511477ffc2a3754cfe668450 1
#511497d3c2a3754cfe66ac3f 1
#5114a199c2a3754cfe66b7ba 1
#51147c8cc2a3754cfe6687ea 1]
	for my_id in ids:
		event = ei.getDocument({'_id':ObjectId(my_id)})
		ei2.addEvent(event)
	
if __name__=='__main__':
	main()

