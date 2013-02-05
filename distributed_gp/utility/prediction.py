import types

class Prediction:
	
	def __init__(self, prediction=None):
		if prediction is None:
			self._prediction = {}
		else:
			if type(prediction) is types.DictType:
				self._prediction = prediction
			else:
				self._prediction = prediction.toJSON()
	
	def getFileName(self):
		return self._prediction['file_name']
	
	def setFileName(self, file_name):
		self._prediction['file_name'] = file_name
	
	def setRegion(self, region):
		# region must be a json, see region.py
		# or an instance of class defined in prediction.py
		if not type(region) is types.DictType:
			region = region.toJSON()
		self._prediction['region'] = region
		
	def setModelUpdateTime(self, model_time):
		# model_time must a string
		self._prediction['model_update_time'] = model_time
	
	def setTime(self, t):
		# created_time must a string
		self._prediction['time'] = t
	
	def setPredictedValues(self, mu, std):
		# std must be the standard deviation, instead of variance
		self._prediction['mu'] = mu
		self._prediction['std'] = std
		
	def toJSON(self):
		return self._prediction