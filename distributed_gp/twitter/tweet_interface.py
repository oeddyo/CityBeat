##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A high level interface to access the alarm data, for labeling the event
##########
#Edited by: (Please write your name here)#

from mongodb_interface import MongoDBInterface
from event import Event
from config import InstagramConfig
from datetime import datetime
from bson.objectid import ObjectId

import config
import time
import logging
import string
import types

class TweetInterface(MongoDBInterface):
	def __init__(self, db=TwitterConfig.tweet_db,  
	             collection=TwitterConfig.tweet_collection):
	  # initialize an interface for accessing event from mongodb
	  super(TweetInterface, self).__init__()
	  self.setDB(db)
	  self.setCollection(collection)