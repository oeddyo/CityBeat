##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A basic and private interface to connect and test the mongo db 
#
##########
#Edited by: (Please write your name here)#

import pymongo


class MongoDBInterface:
	
	def __init__(self, address, port):
		self.connection = pymongo.Connection(address, port)
	
	def SetDB(self, DBName):
		self.db = self.connection[DBName]
		
	def SetCollection(self, collectionName):
		self.collection = self.db[collectionName]
	
	def SaveItem(self, item):
		self.collection.insert(item)
	
	def GetItem(self, condition=None):
		if not condition is None:
			return self.collection.find_one(condition)
		else:
			return self.collection.find_one()
		
	def GetAllItems(self, condition=None):
		if not condition is None:
			return self.collection.find(condition)
		else:
			return self.collection.find()
	
	def UpdateItem(self, item):
		self.collection.update({'_id':item['_id']}, item, True)
		
	def ClearItems(self):
		# do not use this method unless test
		self.collection.remove({})
	
	def TestUpdate(self):
		photos = self.collection.find()
		for photo in photos:
			photo['label'] = 'unlabeled'
			self.collection.update(  {'id':photo['id']}, photo, True )
	
	def TestGroupAndSave(self, records):
		event = {'lat':2, 'lng':1, 'photos':records, 'label':'unlabeled'}
		self.collection.insert(event)




m = MongoDBInterface( 'grande',27017   )
m.SetDB('citybeat')
m.SetCollection('photos')
w = m.GetAllItems({"$and":[{"created_time":{"$lt":"1354459505"}}, {"created_time":{"$gte":"1354459105"}}] })
cnt = 0
for i in w:
    cnt += 1
    print i['location']

print cnt
