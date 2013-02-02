##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A high level interface to access the alarm data, for labeling the event
##########
#Edited by: (Please write your name here)#

from mongodb_interface import MongoDBInterface
from confin import InstagramConfig
from datetime import datetime

import config
import time
import logging
import string

_address = 'grande'
_port = 27017

class EventInterface(MongoDBInterface):
	
	def __init__(self, db=InstagramConfig.event_db,  
	             collection=InstagramConfig.event_collection):
		# initialize an interface for accessing event from mongodb
		super(EventInterface, self).__init__()
		self.setDB(db)
		self.setCollection(collection)
			
	def _mergeTwoEvents(self, odd_event, new_event):
		# merge the photos from the new event to the old event
		# it will remove the duplicate photos
		old_photos = odd_event['photos']
		new_photos = new_event['photos']
		old_photo = old_photos[-1]
		merged = 0
		for i in xrange(0,len(new_photos)):
			if self._unicodeToInt(new_photos[i]['created_time']) > self._unicodeToInt(old_photo['created_time']):
				old_photos = old_photos + new_photos[i:]
				print '%d out of %d photos have been increased' %(len(new_photos[i:]), len(new_photos))
				merged = 1
				break
			
		if not merged:
			print 'No photo has been increased'
		
		odd_event['photos'] = old_photos
		return odd_event
	
	def _unicodeToInt(self, unic):
		return string.atoi(unic.encode("utf-8"))
		
	def mergeEvent(self, event):
		# merge the event with an elder in DB
		
		# get all events in the same location
		all_events = self._getAllEventsAtLocation(event['mid_lat'], event['mid_lng'])
		if all_events is None:
			return False
		for odd_event in all_events:
			# find a proper old event to combine (we assume there is only one "proper" old event)
			last_photo = odd_event['photos'][-1]
			t1 = self._unicodeToInt(event['photos'][-1]['created_time'])
			t2 = self._unicodeToInt(last_photo['created_time'])
			
			if t1 == t2:
				# no further photos for this event
				return True
			
			# maximal allowed time interval is 15 mins
			if t1 > t2 and t1 <= t2 + InstagramConfig.merge_time_interval:
				#within 15 minutes
				merged_event = self._mergeTwoEvents(odd_event, event)
				self.updateDocument(merged_event)
				return True
		return False
				

		

#def getPhotoFromInstagram(cnt):
#	# only for test
#	cur_time = datetime.utcnow()
#	#sw_ne = (40.773012,-73.9863145)
#	sw_ne = (40.75953, -73.9863145)
#	lat = sw_ne[0]
#	lon = sw_ne[1]
#	client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)
#	try:
#		res = client.media_search(lat = lat, lng = lon, return_json = True, distance = 1*1000, count=cnt)
#		return res
#	except Exception as e:
#		print 'Exception!'
#		logging.warning(e)
#	return None
#
#
#def TestWithFakeItems():
#	myDB = MongoDBInterface(dbAddress, 27017)
#	myDB.SetDB('alarm_filter')
#	myDB.SetCollection('photos')
#	for i in xrange(2):
#		photos = getPhotoFromInstagram(2)
#		myDB.SaveItem({'label':'unlabeled', 'photo':photos, 'test':'test'})
#	testDB = AlarmDataInterface(dbAddress, 27017)
#	i = 0
#	while True:
#		event = testDB.GetUnlabeledEvent()
#		if event is None:
#			break
#		testDB.LabelEvent(event, 'fake')
#		i = i + 1
#		print i
#	
#	
#def main():
#	# main() function is only for test
#	TestWithFakeItems()
#
#if __name__ == "__main__":
#	main()
