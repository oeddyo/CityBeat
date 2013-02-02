from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface
from bson.objectid import ObjectId
from EventQuery import CaptionParser
from EventQuery import EventQuery
from Photo import Photo


import operator
import math
import nltk
import random

class Event:
	def __init__(self, event):
		self._event = event
		
	def GetAverageLocationOfPhotos(self):
		photos = self._event['photos']
		lat = 0
		lng = 0
		n = 0
		for photo in photos:
			pLat = float(photo['location']['latitude'])
			pLon = float(photo['location']['longitude'])
			lat += pLat
			lng += pLon
			n += 1
		return lat/n, lng/n
		
	def GetZscore(self):
		return (float(self._event['actual_value']) - float(self._event['predicted_mu'])) / float(self._event['predicted_std'])
	
	def _GetClosenessOfPhotosByGeolocation(self):
		
		def DisBetweenPhotos(photo1, photo2):
			# is there any precision issue?
			lat1 = float(photo1['location']['latitude'])
			lon1 = float(photo1['location']['longitude'])
			lat2 = float(photo2['location']['latitude'])
			lon2 = float(photo2['location']['longitude'])
			return math.sqrt(10000*(lat1-lat2)*(lat1-lat2) + 10000*(lon1-lon2)*(lon1-lon2))
			
		photos = self._event['photos']
		n = len(photos)
		avgDis = 0
		
		for i in xrange(0, n):
			disToOtherPhotos = 0
			for j in xrange(0, n):
				if not i == j:
					disToOtherPhotos += DisBetweenPhotos(photos[i], photos[j])
			avgDis += disToOtherPhotos / (n - 1)
			
		return avgDis / n
		
	def _GetAvgLenOfCaption(self):
		numberOfPhotosWithCaption = 0
		captionLens = 0
		photos = self._event['photos']
		for photo in photos:
			if not photo['caption'] is None:
				if not photo['caption']['text'] is None:
					lenOfCaption = len(photo['caption']['text'])
					if lenOfCaption > 0:
						captionLens += lenOfCaption
						numberOfPhotosWithCaption += 1
		if numberOfPhotosWithCaption == 0:
			return -1, 0
		else:
			return 1.0 * captionLens / numberOfPhotosWithCaption, numberOfPhotosWithCaption
		
	def _GetTopWordList(self, k):
		cp = CaptionParser()
		photos = self._event['photos']
		for photo in photos:
			p = Photo(photo)
			cp.InsertCaption(p.GetCaption())
		topWords = cp.GetTopWords(k)
		return topWords
	
	def _KTopWordsPopularity(self, k=1):
		# compute the average popularity of k-top words
		topWords = self._GetTopWordList(k)
		avgPop = 0
		for topWord in topWords:
			avgPop += topWord[1]
		return avgPop / min(k, len(topWords))
		
	def _GetPercentageOfStopwordsFromTopWords(self, k=10):
		# compute the percentage of stopwords in all k-top words
		topWords = self._GetTopWordList(k)
		stopwords = nltk.corpus.stopwords.words('english') 

		cnt = 0
		for topWord in topWords:
			if topWord[0] in stopwords:
				cnt += 1
		# if no caption, output as all stopwords
		if len(topWords) == 0:
			return 1
		return 1.0 * cnt / min(k, topWords)
				
	
	def ExtractFeatures(self):
		label = int(self._event['label'])
		zscore = self.GetZscore()
		std = float(self._event['predicted_std'])
		numberOfPhotos = len(self._event['photos'])
		closenessOfGeolocation = self._GetClosenessOfPhotosByGeolocation()
		captions = self._GetAvgLenOfCaption()
		avgLenOfAllCaptions = captions[0]
		numberOfPhotosWithCaption = captions[1]
		TopWordsPopularity = self._KTopWordsPopularity(1)
		percentageOfStopWords = self._GetPercentageOfStopwordsFromTopWords(10)
		return label, [zscore, std, numberOfPhotos, closenessOfGeolocation,
		               avgLenOfAllCaptions, numberOfPhotosWithCaption, TopWordsPopularity, 
		               percentageOfStopWords]


def GenerateArffFileHeader():
	print '@relation CityBeatEvents'
	print '@attribute zscore real'
	print '@attribute std real'
	print '@attribute numberOfPhotos real'
	print '@attribute closenessOfGeolocation real'
	print '@attribute avgLenOfAllCaptions real'
	print '@attribute numberOfPhotosWithCaption real'
	print '@attribute TopWordsPopularity real'
	print '@attribute percentageOfStopWords real'
	print '@attribute label {1,-1}'
	print '@data'
	

def main():
	
	eq = EventQuery('grande', 27017)
	eq.SetDB('historic_alarm')
	eq.SetCollection('labeled_event')
	
	conditions = {}
	events = eq.GetAllItems()
	
	GenerateArffFileHeader()
	
	
	trueEvents = []
	falseEvents = []
	
	for event in events:
		e = Event(event)
		features = e.ExtractFeatures()
		if features[0] == -1:
			falseEvents.append(features[1])
		else:
			trueEvents.append(features[1])
			
	random.shuffle(falseEvents)
	
	n = len(trueEvents)
	
	for i in xrange(0, n):
		for j in xrange(0, len(trueEvents[i])):
			print trueEvents[i][j],',',
		print 1
		
		for j in xrange(0, len(falseEvents[i])):
			print falseEvents[i][j],',',
		print -1
		
			
		

		
		
#	
#	lat = []
#	lng = []
#	
#	for event in events:
#		e = Event(event)
#		location = e.GetAverageLocationOfPhotos()
#		lat.append(location[0])
#		lng.append(location[1])
#	
#	for i in xrange(0, len(lat)):
#		print lat[i],',',lng[i]
#	
#	cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#	
#	for event in events:
#		nPhotos = len(event['photos'])
#		cnt[nPhotos/10] = cnt[nPhotos/10] + 1
#		
#	print cnt
	


#	eq = EventQuery('grande', 27017)
#	eq.SetDB('historic_alarm')
#	eq.SetCollection('raw_event')
#	created_time = ''
#	lat = '40.768518'
#	lng = '-73.9931535'
#	conditions = {'lat':lat, 'lng':lng}
#	conditions = {'created_time':'2013-01-09 17:57:09.798046'}
#	event = eq.GetItem(conditions)
#	captionParser = CaptionParser()
#	for photo in event['photos']:
#		if not photo['caption'] is None:
#			caption = photo['caption']['text']
#			captionParser.InsertCaption(caption)
#	topWords = captionParser.GetTopWords(10)
#	words = []
#	freq = []
#	for word in topWords:
#		words.append(word[0])
#		freq.append(word[1])
#	for word in words:
#		print "'" + word + "',",
#	print
#	
#	for freq in freq:
#		print freq,
#	print


if __name__ == '__main__':
	main()
	
	
	

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