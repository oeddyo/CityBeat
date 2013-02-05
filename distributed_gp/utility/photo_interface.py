import config
import time
import logging
import string
import types

from datetime import datetime
from mongodb_interface import MongoDBInterface
from config import InstagramConfig

class PhotoInterface(MongoDBInterface):
	
	def __init__(self, db=InstagramConfig.photo_db,  
	             collection=InstagramConfig.photo_collection):
		# initialize an interface for accessing photos from mongodb
		super(PhotoInterface, self).__init__()
		self.setDB(db)
		self.setCollection(collection)
	
	def rangeQuery(self, region=None, period=None):
		#period should be specified as: [begin_time end_time]
		#specify begin_time and end_time as the utctimestamp, string!!
		
		
		region_conditions = {}
		period_conditions = {}
		if not region is None:
		#region should be specified as the class defined in region.py
			if not type(region) is types.DictType:
				region = region.toJSON() 
			region_conditions = {'location.latitude':{'$gte':region['min_lat'], '$lte':region['max_lat']},
				                   'location.longitude':{'$gte':region['min_lng'], '$lte':region['max_lng']}
				                   	}
				                   	
		if not period is None:
			period_conditions = {'created_time':{'$gte':period[0], '$lte':period[1]}}

		conditions = dict(region_conditions, **period_conditions)
		
		#returns a cursor
		#sort the photo in chronologically decreasing order
		return self.getAllDocuments(conditions).sort('created_time', 1)
	
	def _computeBoundaryOfPhotos(self):
		cnt = 0
		min_lat = 1000
		min_lng = 1000
		max_lat = -1000
		max_lng = -1000
		photos = self.getAllDocuments()
		print type(photos)
		for photo in photos:
			cnt += 1
			if photo['location'] is None:
				continue
			lat = float(photo['location']['latitude'])
			lng = float(photo['location']['longitude'])
			max_lat = max(max_lat, lat)
			min_lat = min(min_lat, lat)
			max_lng = max(max_lng, lng)
			min_lng = min(min_lng, lng)
			if cnt % 10000 == 0:
				print cnt
		return [min_lat, max_lat, min_lng, max_lng]
	


if __name__=="__main__":
	pass
	  