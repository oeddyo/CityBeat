from mongodb_interface import MongoDBInterface
from photo import Photo
from region import Region

import operator
import string
import types


def unicodeToInt(self, unic):
	return string.atoi(unic.encode("utf-8"))

class Event(object):
	
	def __init__(self, event=None):
		# the input argument event should be a json, dictionary
		if not event is None:
			if type(event) is types.DictType:
				self._event = event
			else:
				self._event = event.toJSON()
		else:
			# create a new event
			self._event = {'photos':[], 'label':'unlabeled'}
				
	def addPhoto(self, photo):
		# when use this method, please keep adding photo in chronologically increasing order
		if not type(photo) is types.DictType:
			photo = photo.toJSON()
		self._event['photos'].append(photo)
		
	def getPhotoNumber(self):
		return len(self._event['photos'])
	
	def getLabel(self):
		return self._event['label']
	
	def getRegion(self):
		return self._event['region']
	
	def getZscore(self):
		if 'zscore' in self._event.keys():
			return self._event['zscore']
		else:
			return (self._event['predicted_mu'] - self._event['actual_value']) / self._event['predicted_std']
	
	def mergeWith(self, event):
		if not type(event) is types.DictType:
			event = event.toJSON()
		last_photo = self._event['photos'][-1]
		last_photo_time = unicodeToInt(last_photo['created_time'])
		
		new_photos = event['photos']
		merged = 0
		for photo in new_photos:
			created_time = unicodeToInt(photo['created_time'])
			# the if clause has a potential and little bug, but too rare too happen
			if created_time > last_photo_time:
				self.addPhoto(photo)
				merged += 1
		return merged
				
	def setRegion(self, region):
		if not type(region) is types.DictType:
			region = region.toJSON()
		self._event['region'] = r.toJSON()
	
	def setPhotos(self, photos):
		# a set of json objects
		self._event['photos'] = photos
		
	def setCreatedTime(self, utc_time):
		self._event['created_time'] = utc_time
		
	def setPredictedValues(self, mu, std):
		self._event['predicted_mu'] = mu
		self._event['predicted_std'] = std
		
	def setZscore(self, zscore):
		self._event['zscore'] = zscore
		
	def setActualValue(self, actual_value):
		self._event['actual_value'] = actual_value
	
	def setLabel(self, label='unlabeled'):
		self._event['label'] = label
	
	def toJSON(self):
		return self._event
		
def main():
	pass
	
	

# http://www.nba.com/games/20130107/BOSNYK/gameinfo.html   basketball event
# even we can know when start
# 2013-01-07 19:31:33.087495
# 40.750542 , -73.9931535

# the basketball on Jan 10th was not detected

# the basketball on Jan 11th was detected but with wrong date


#2013-01-12 01:01:05.757332 40.750542 -73.9931535
#http://instagr.am/p/UXTRztp4zv/ 40.750489767 -73.993270272 1
#http://instagr.am/p/UXTS4UymD0/ 40.7512982 -73.992291518 -1
#http://instagr.am/p/UXTZChsnjw/ 40.75011444 -73.992973327 1
#http://instagr.am/p/UXTb5-JVpf/ 40.749865723 -73.991356529 1
#http://instagr.am/p/UXTb2svJVR/ 40.750333333 -73.993333333 1
#http://instagr.am/p/UXTjT5HJ-a/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXTjdOTHiP/ 40.750316079 -73.993385875 1
#http://instagr.am/p/UXTjzdLbrP/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXTlcyuxST/ 40.7505 -73.993166666 1
#http://instagr.am/p/UXToQPgHKE/ 40.7505 -73.993333333 1
#http://instagr.am/p/UXToNDLPJa/ 40.753426253 -73.992566983 -1
#http://instagr.am/p/UXTohpoWM5/ 40.750516261 -73.993499279 0
#http://instagr.am/p/UXToxPL-KD/ 40.750022888 -73.9919281 1
#http://instagr.am/p/UXTw3uMYK3/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXTy1ouFIu/ 40.750499725 -73.993164062 1
#http://instagr.am/p/UXTzMyveR9/ 40.749858347 -73.991703037 -1
#http://instagr.am/p/UXT02igOax/ 40.7535 -73.992833333 -1
#http://instagr.am/p/UXT6EKHYiF/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXT7AUEver/ 40.751074424 -73.991849624 -1
#http://instagr.am/p/UXT7KsExpE/ 40.750999999 -73.993666666 0
#http://instagr.am/p/UXT8rMyDnu/ 40.750333333 -73.993333333 1
#http://instagr.am/p/UXT-S_IFkk/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXUAX7yM6C/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXUAzODrWE/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXUBRlmXNj/ 40.7514678 -73.9917506 -1
#http://instagr.am/p/UXUF_Bi-ME/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXUGcnudpN/ 40.750404833 -73.993007524 1
#http://instagr.am/p/UXUIHZQ4L8/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXUITdOHrp/ 40.750468278 -73.993285868 1
#http://instagr.am/p/UXUJWBpIG8/ 40.750300357 -73.993121214 1
#http://instagr.am/p/UXUKdUgaNx/ 40.750833333 -73.993499999 1
#http://instagr.am/p/UXUMcWPQ9v/ 40.7505 -73.993499999 1
#http://instagr.am/p/UXUN5Mk_2c/ 40.75 -73.992833333 0
#http://instagr.am/p/UXUUU8i6oA/ 40.750680008 -73.993747246 1
#http://instagr.am/p/UXUVu_q4JP/ 40.750516261 -73.993499279 1
#http://instagr.am/p/UXUV_mw0I6/ 40.7505 -73.993499999 1
#http://instagr.am/p/UXUW3mPSx2/ 40.749859206 -73.989961523 -1
#http://instagr.am/p/UXUcQWu0B5/ 40.75113422 -73.994260727 1
#http://instagr.am/p/UXUc3rhCPt/ 40.751132965 -73.994262695 1
#http://instagr.am/p/UXUeOKHrme/ 40.750553131 -73.993774414 -1