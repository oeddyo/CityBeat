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
import types

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
		# document must be a json or a class from {event, photo, prediction}
		if not type(document) is types.DictType:
			document = document.toJSON()
		self._collection.save(document)
	
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
		if not type(document) is types.DictType:
			document = document.toJSON()
		self._collection.update({'_id':document['_id']}, document, True)
			
	def getAllDocumentIDs(self):
		# 333
		IDs = []
		query_res = self._collection.find({},{'_id':1})
		for ID in query_res:
			IDs.append(ID['_id'])
		return IDs


if __name__=='__main__':
	mi = MongoDBInterface()
	mi.setDB('historic_alarm')
	mi.setCollection('labeled_event')
	print mi.getAllDocumentIDs()
	