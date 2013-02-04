from mongodb_interface import MongoDBInterface
from AlarmInterface import AlarmDataInterface
import operator
from bson.objectid import ObjectId



class EventQuery(MongoDBInterface):
	
	def __init__(self, address, port):
		super(EventQuery, self).__init__(address, port)
	
	def _CheckPhoto(self, photo, word):
		if word is None:
			return True
		if not photo['caption'] is None:
			text = photo['caption']['text']
			if word in text:
				return True
		return False


	def QueryEventsByKeyword(self, conditions=None, word=None, limit=-1):
		allEvents = self.GetAllItems(conditions)
		validEvents = []
		for event in allEvents:
			if len(validEvents) >= limit and not limit == -1:
				return validEvents
			for photo in event['photos']:
				if self._CheckPhoto(photo, word):
					validEvents.append(event)
					break
		return validEvents
		
	def QueryPhotosByKeyword(self, conditions=None, word=None):
		photoURLs = []
		allEvents = self.GetAllItems(conditions)
		for event in allEvents:
			for photo in event['photos']:
				if self._CheckPhoto(photo, word):
					photoURLs.append(photo['link'])
		return photoURLs			


class CaptionParser:
	
	def __init__(self):
		self.wordDict = {}
		self.dn = 0  # number of documents accumulated
	
	def GetTopWords(self, k=-1):
		topWords = sorted(self.wordDict.iteritems(), key=operator.itemgetter(1), reverse=True)
		for i in xrange(0, len(topWords)):
			tmpTuple = (topWords[i][0], 1.0*topWords[i][1] / self.dn)
			topWords[i] = tmpTuple
		return topWords[0:min(k, len(topWords))]
	
	def InsertCaption(self, cap):
		if cap is None or len(cap) == 0:
			return
		self.dn = self.dn + 1
		tmpDict = self._PreprocessCaption(cap)
		for word in tmpDict.keys():
			if word in self.wordDict.keys():
				self.wordDict[word] = self.wordDict[word] + 1
			else:
				self.wordDict[word] = 1
	
	def _PreprocessCaption(self, cap):
		tmpDict = {}
		words = cap.lower().split(' ')
		for word in words:
			newWord = self._ExtractWord(word)
			if len(newWord) == 0:
				continue
			if newWord in tmpDict.keys():
				tmpDict[newWord] = tmpDict[newWord] + 1
			else:
				tmpDict[newWord] = 1
		return tmpDict
	
	def _ExtractWord(self, word):
		newWord = ''
		for c in word:
			if c >= 'a' and c<='z':
				newWord = newWord + c
		return newWord
		

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

def main():
	
	
	
	eq = EventQuery('grande', 27017)
	eq.SetDB('historic_alarm')
	eq.SetCollection('raw_event')
	
	events = eq.GetAllItems()
	
	Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	T = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	
	for event in events:
		e = Event(event)
		zscore = int(round(e.GetZscore()))
		if e.GetZscore() < 3:
			print e.GetZscore()
		ind = min(10, zscore)
		Z[ind] += 1
		if event['label'] == '1':
			T[ind] += 1
	
	print Z
	print T
		
		
		
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