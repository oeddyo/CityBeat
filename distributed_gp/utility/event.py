from mongodb_interface import MongoDBInterface
from photo import Photo
from region import Region

import operator
import string
import types

class Event(object):
	
	def __init__(self, event=None):
		# the input argument event should be a json, dictionary
		if not event is None:
			if type(event) is types.DictType:
				self._event = event
			else:
				self._event = event.toJSON()
				
			# preprocess, to correct the data
			self.setActualValue(self._getActualValueByCounting())
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
		
	def getActualValue(self):
		return self._event['actual_value']
	
	def _getActualValueByCounting(self):
		user_ids = set()
		for photo in self._event['photos']:
			user_ids.add(int(photo['user']['id']))
		self.setActualValue(len(user_ids))
		return len(user_ids)
	
	def getRegion(self):
		return self._event['region']
		
	def selectOnePhotoForOneUser(self):
		# a strong filter
		user_ids = set()
		photos = self._event['photos']
		new_photos = []
		for photo in photos:
			user_id = photo['user']['id']
			if user_id in user_ids:
				continue
			user_ids.add(user_id)
			new_photos.append(photo)
		self._event['photos'] = new_photos
	
	def removeDuplicatePhotos(self):
		# this method is not good, just for tempory use
		# by judging if the caption is duplicate
		new_photos = []
		num_duplicate = 0
		for photo in self._event['photos']:
			p = Photo(photo)
			is_duplicate = False
			cap1 = p.getCaption()
			user1 = p.getUserName()
			for new_photo in new_photos:
				p2 = Photo(new_photo)
				cap2 = p2.getCaption()
				user2 = p2.getUserName()
				if user1 == user2 and (len(cap1)>0 and cap1 == cap2):
					is_duplicate = True
					num_duplicate += 1
					break
			if not is_duplicate:
				new_photos.append(photo)
				
		if num_duplicate > 0:
			self._event['photos'] = new_photos
			
		return num_duplicate
		
	def getPhotosbyKeyword(self, word):
		# return a list of photos containg the word
		res_photo = []
		for photo in self._event['photos']:
			cap = Photo(photo).getCaption()
			if cap is None:
				continue
			cap = cap.lower()
			if word in cap:
				res_photo.append(photo)
		return res_photo
	
	def getZscore(self):
		if 'zscore' in self._event.keys():
			return self._event['zscore']
		else:
			return (float(self._event['actual_value']) - float(self._event['predicted_mu'])) / float(self._event['predicted_std'])
	
	def sortPhotos(self):
		# this sorting can prevent bugs when merging
		photo_list = []
		for photo in self._event['photos']:
			photo_list.append([photo, int(photo['created_time']), str(photo['id'])])
		photo_list.sort(key=operator.itemgetter(1, 2), reverse=True)
		self._event['photos'] = [row[0] for row in photo_list]
	
	def mergeWith(self, event):
		if type(event) is types.DictType:
			event = Event(event)
		event = event.toJSON()
		
		photo_list1 = self._event['photos'] 
		photo_list2 = event['photos']
		
		new_photo_list = []
		l1 = 0
		l2 = 0
		merged = 0
		while l1 < len(photo_list1) and l2 < len(photo_list2):
			p1 = Photo(photo_list1[l1])
			p2 = Photo(photo_list2[l2])
			compare = p1.compare(p2)
			if compare == 1:
				new_photo_list.append(photo_list1[l1])
				l1 += 1
				continue
			
			if compare == -1:
				new_photo_list.append(photo_list2[l2])
				l2 += 1
				merged += 1
				continue
			
			# compare == 0
			new_photo_list.append(photo_list1[l1])
			l1 += 1
			l2 += 1
		
		while l1 < len(photo_list1):
			new_photo_list.append(photo_list1[l1])
			l1 += 1
		
		while l2 < len(photo_list2):
			new_photo_list.append(photo_list2[l2])
			l2 += 1
			merged += 1
		
		self._event['photos'] = new_photo_list
		# update actual value
		self.setActualValue(self._getActualValueByCounting())
		
		# do not change the order of the following code
		actual_value_1 = self._event['actual_value']
		actual_value_2  = event['actual_value']
		zscore1 = float(self._event['zscore'])
		zscore2 = float(event['zscore'])
		std1 = float(self._event['predicted_std'])
		std2 = float(event['predicted_std'])
		new_std = (std1 * actual_value_1 + std2 * actual_value_2) / (actual_value_1 + actual_value_2)
		new_zscore = (zscore1 * actual_value_1 + zscore2 * actual_value_2) / (actual_value_1 + actual_value_2)
		self.setZscore(new_zscore)
		new_mu = actual_value_1 - new_zscore * new_std
		self.setPredictedValues(new_mu, new_std)
		
		return merged
				
	def setRegion(self, region):
		if not type(region) is types.DictType:
			region = region.toJSON()
		self._event['region'] = region
	
	def setPhotos(self, photos):
		# a set of json objects
		self._event['photos'] = photos
		
	def setCreatedTime(self, utc_time):
		self._event['created_time'] = str(utc_time)
		
	def setPredictedValues(self, mu, std):
		self._event['predicted_mu'] = float(mu)
		self._event['predicted_std'] = float(std)
		
	def setZscore(self, zscore):
		self._event['zscore'] = float(zscore)
		
	def setActualValue(self, actual_value):
		self._event['actual_value'] = int(actual_value)
	
	def setLabel(self, label='unlabeled'):
		self._event['label'] = label
	
	def toJSON(self):
		return self._event
		
	def _test_print(self):
		print self._event['created_time'], 'photos:'
		for photo in self._event['photos']:
			print photo['created_time']
			
	def getLatestPhotoTime(self):
		lt = int(self._event['photos'][0]['created_time'])
		for photo in self._event['photos']:
			t = int(photo['created_time'])
			if t > lt:
				lt = t
		return lt
		
	   
	def getEarliestPhotoTime(self):
		et = int(self._event['photos'][-1]['created_time'])
		for photo in self._event['photos']:
			t = int(photo['created_time'])
			if t < et:
				et = t
		return et
		
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