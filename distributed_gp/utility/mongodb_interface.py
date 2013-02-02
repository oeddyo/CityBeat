##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A basic and private interface to connect and test the mongodb 
#
##########
#Edited by: (Please write your name here)#

from config import InstagramConfig

import pymongo
import config

class MongoDBInterface(object):
	#A basic interface#
	
	def __init__(self):
		self._connection = pymongo.Connection(config.mongodb_address,
																					config.mongodb_port)
														
	def setDB(self,  name):
		self._db = self._connection[name]
		
	def setCollection(self, name):
		self._collection = self._db[name]
	
	def saveDocument(self, document):
		self._collection.insert(document)
	
	def getDocument(self, condition=None):
		if not condition is None:
			return self._collection.find_one(condition)
		else:
			return self._collection.find_one()
		
	def getAllDocuments(self, condition=None):
		if not condition is None:
			return self._collection.find(condition)
		else:
			return self._collection.find()
	
	def updateDocument(self, document):
		self._collection.update({'_id':document['_id']}, document, True)

