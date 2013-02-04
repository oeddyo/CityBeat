import config
import types

from datetime import datetime
from mongodb_interface import MongoDBInterface
from config import InstagramConfig

class PredictionInterface(MongoDBInterface):
	
	def __init__(self, db=InstagramConfig.prediction_db,  
	             collection=InstagramConfig.prediction_collection):
		# initialize an interface for accessing photos from mongodb
		super(PredictionInterface, self).__init__()
		self.setDB(db)
		self.setCollection(collection)
		
	def getMostRecentPrediction(self, region):
		# TODO: within one hour
		# region should an instance of the class Region defined in region.py
		if not type(region) is types.DictType:
			region = region.toJSON()
		predictions = self.getAllDocuments({'region':region}).sort('time', -1)
		for prediction in predictions:
			return prediction
		raise Exception('no prediction is found')
		
	def getNearestPrediction(self, region, utc_time):
		# given t, find the most nearest prediction whose time is greater than or equal to t.
		# utc_time should a string (or unicode)
		if not type(region) is types.DictType:
			region = region.toJSON()
		utc_time = str(utc_time)
		predictions = self.getAllDocuments({'region':region, 'time':{'$gte':utc_time}}).sort('time', 1)
		for prediction in predictions:
			# only need to judge the first one
			if int(prediction['time']) - 3600 <= int(utc_time):
				return prediction
			return None
		return None

if __name__=="__main__":
	pass
