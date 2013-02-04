from event_interface import EventInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser

import operator
import string
import types
import math
import nltk

class EventFeature(Event):
	# this class is the extension of class Event, especially for feature extraction
	# to prevent the class Event from being too long to read
	
	def __init__(self, event):
		super(EventFeature, self).__init__(event)
				
	def _getPhotoAvgLocation(self):
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
		
	def _getTopWords(self, k=1):
		caption_parser = CaptionParser()
		for photo in self._event['photos']:
			p = Photo(photo)
			caption = p.getCaption()
			if not caption is None:
				caption_parser.insertCaption(caption)
		return caption_parser.getTopWords(k)
	
	def extractFeatures(self):
		avg_cap_len = self.getAvgCaptionLen()
		avg_photo_dis = self.getAvgPhotoDis()
		cap_num = self.getCaptionNumber()
		photo_num = self.getPhotoNumber()
		stop_word_per = self.getPercentageOfStopwordsFromTopWords()
		std = self.getPredictedStd()
		mu = self.getPredictedMu()
		top_word_pop = self.getTopWordPopularity()
		zscore = self.getZscore()
		entropy = self.getEntropy(5,5)
		
		label = self.getLabel()
		
		return [avg_cap_len, avg_photo_dis, cap_num, photo_num, stop_word_per,
		        std, mu, top_word_pop, zscore, entropy, label]
	
	def GenerateArffFileHeader(self):
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
		
	def getAvgPhotoDis(self):
		# actually we get the distance between photos, instead of closeness
		
		def photoDistance(photo1, photo2):
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
			dis_to_other_photo = 0
			for j in xrange(0, n):
				if not i == j:
					dis_to_other_photo += photoDistance(photos[i], photos[j])
			avgDis += dis_to_other_photo / (n - 1)
			
		return avgDis / n
	
	def getAvgCaptionLen(self):
		cap_number = 0
		cap_lens = 0
		photos = self._event['photos']
		for photo in photos:
			photo = Photo(photo)
			cap_len = len(photo.getCaption())
			if cap_len > 0:
				cap_lens += cap_len
				cap_number += 1
		if cap_number == 0:
			return -1
		else:
			return 1.0 * cap_lens / cap_number
	
	def getCaptionNumber(self):
		cap_number = 0
		photos = self._event['photos']
		for photo in photos:
			photo = Photo(photo)
			cap_len = len(photo.getCaption())
			if cap_len > 0:
				cap_number += 1
		return cap_number
		
	def getTopWordPopularity(self, k=2):
		# compute the average popularity of k-top words
		top_words = self._getTopWords(k)
		avg_pop = 0
		for top_word in top_words:
			avg_pop += top_word[1]
		return avg_pop / min(k, len(top_words))
		
	def getPercentageOfStopwordsFromTopWords(self, k=10):
		# compute the percentage of stopwords in all k-top words
		top_words = self._getTopWords(k)
		stopwords = nltk.corpus.stopwords.words('english') 
		cnt = 0
		for top_word in top_words:
			if top_word[0] in stopwords:
				cnt += 1
		# if no caption, output as all stopwords
		if len(top_words) == 0:
			return 1
		return 1.0 * cnt / min(k, top_words)
	
	def getPredictedStd(self):
		return self._event['predicted_std']
		
	def getPredictedMu(self):
		return self._event['predicted_mu']
		
	def getEntropy(self, n, m):
		# devide the region into n*m grids to compute the entropy
		# p(i) = # of photos in that grid, to the total number of grids
		photo_number = self.getPhotoNumber()
		region = Region(self._event['region'])
		subregions = region.divideRegion(n,m)
		
		cnt = {}
		for subregion in subregions:
			cnt[subregion] = 0
			
		photos = self._event['photos']
		for photo in photos:
			lat = photo['location']['latitude']
			lng = photo['location']['longitude']
			flag = False
			for subregion in subregions:
				if subregion.insideRegion([lat, lng]):
					cnt[subregion] += 1
					if flag == True:
						raise Exception('bad data')
					flag = True
# lat = 0.004494
# lng = 0.006839

#   40.701108,-73.9931535,54
#   40.705602,-73.9931535,55
#   40.777506,-73.9931535,55
#   40.782,-73.9931535,15
#   40.786494,-73.9931535,15
#   40.795482,-73.9931535,14


40.782,-73.9794755,52
40.782,-73.9726365
40.782,-73.9657975
40.782,-73.9521195
40.782,-73.9452805,51

#		40.799976,-73.9931535,14
#   40.80447,-73.9931535,14
					
		
if __name__=='__main__':
	ei = EventInterface()
	ei.setDB('alarm_filter')
	ei.setCollection('photos')
	
	candidate_events = ei.getAllDocuments()
	for ce in candidate_events:
		event = EventFeature(ce)
		print event.extractFeatures()