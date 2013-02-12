from event_interface import EventInterface
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords

import operator
import string
import types
import random
import math

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
		
	def _getTopWords(self, k=1, stopword_removal=False):
		caption_parser = CaptionParser(stopword_removal=stopword_removal)
		for photo in self._event['photos']:
			p = Photo(photo)
			caption = p.getCaption()
			if not caption is None:
				caption_parser.insertCaption(caption)
		return caption_parser.getTopWords(k)
	
	def extractFeatures(self, entropy_para):
		avg_cap_len = self.getAvgCaptionLen()
		avg_photo_dis = self.getAvgPhotoDis()
		cap_per = self.getCaptionPercentage()
		people_num = self.getActualValue()
		stop_word_per = self.getPercentageOfStopwordsFromTopWords()
		std = self.getPredictedStd()
		top_word_pop = self.getTopWordPopularity()
		zscore = self.getZscore()
		entropy = self.getEntropy(entropy_para)
		ratio = self.getRatioOfPeopleToPhoto()
		
		label = int(self.getLabel())
		event_id = str(self._event['_id'])
		
		
		historic_features = self.getHistoricFeatures(entropy_para)
		diff_avg_photo_dis = avg_photo_dis - historic_features[0]
		diff_top_word_pop = top_word_pop - historic_features[1]
#		diff_entropy = entropy - historic_features[2]
		diff_entropy = historic_features[2]
		diff_avg_cap_len = avg_cap_len - historic_features[3]
		diff_ratio = ratio - historic_features[4]
		
#				return [event.getAvgPhotoDis(), event.getTopWordPopularity(),
#		        event.getEntropy(entropy_para),
#		        event.getAvgCaptionLen(), event.getRatioOfPeopleToPhoto()]
		
		return [avg_cap_len, avg_photo_dis, cap_per, people_num, stop_word_per,
		        std, top_word_pop, zscore, entropy, ratio,
		        diff_avg_photo_dis, diff_top_word_pop, diff_entropy,
		        diff_avg_cap_len, diff_ratio,
		        event_id, label]
		        
	@staticmethod
	def GenerateArffFileHeader():
		print '@relation CityBeatEvents'
		print '@attribute AvgCaptionLen real'
		print '@attribute AvgPhotoDis real'
		print '@attribute CaptionPercentage real'
		print '@attribute PeopleNumber real'
		print '@attribute PercentageOfStopwordsFromTopWords real'
		print '@attribute PredictedStd real'
		print '@attribute TopWordPopularity real'
		print '@attribute Zscore real'
		print '@attribute Entropy real'
		print '@attribute TheRatioOfPeopleToPhoto real'
		print '@attribute diff_AvgPhotoDis real'
		print '@attribute diff_TopWordPopularity real'
		print '@attribute diff_Entropy real'
		print '@attribute diff_AvgCaptionLen real'
		print '@attribute diff_TheRatioOfPeopleToPhoto real'
												
		print '@attribute event_id string'
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
	
	def getCaptionPercentage(self):
		cap_number = 0
		photos = self._event['photos']
		for photo in photos:
			photo = Photo(photo)
			cap_len = len(photo.getCaption())
			if cap_len > 0:
				cap_number += 1
		return cap_number * 1.0 / len(photos)
		
	def getTopWordPopularity(self, k=1):
		# compute the average popularity of k-top words
		top_words = self._getTopWords(k, True)
		avg_pop = 0
		for top_word in top_words:
			avg_pop += top_word[1]
		return avg_pop / min(k, len(top_words))
		
	def getPercentageOfStopwordsFromTopWords(self, k=5):
		# compute the percentage of stopwords in all k-top words
		top_words = self._getTopWords(k, False)
		stopwords = Stopwords.stopwords() 
		cnt = 0
		for top_word in top_words:
			if top_word[0] in stopwords:
				cnt += 1
		# if no caption, output as all stopwords
		if len(top_words) == 0:
			return 1
		return 1.0 * cnt / min(k, top_words)
	
	def getPredictedStd(self):
		return float(self._event['predicted_std'])
		
	def getPredictedMu(self):
		return float(self._event['predicted_mu'])
		
	def _getEntropy(self, n):
		# devide the region into n*m grids to compute the entropy
		# p(i) = # of photos in that grid, to the total number of grids
		# it returns the list of subregions associated with the number photos falling into that region
		photo_number = self.getPhotoNumber()
		region = Region(self._event['region'])
		subregions = region.divideRegions(n, n)
		
		cnt = [0]*n*n
			
		photos = self._event['photos']
		for photo in photos:
			lat = photo['location']['latitude']
			lng = photo['location']['longitude']
			flag = False
			i = 0
			for subregion in subregions:
				if subregion.insideRegion([lat, lng]):
					cnt[i] += 1
					if flag == True:
						raise Exception('bad data')
					flag = True
				i += 1
		return cnt
		
		
	def getEntropy(self, n):
		# devide the region into n*m grids to compute the entropy
		# p(i) = # of photos in that grid, to the total number of grids
		cnt = self._getEntropy(n)
		# h(x) = sum(p(x)*log(p(x))
		photo_number = self.getPhotoNumber()
		h = 0
		for num in cnt:
			if num == 0:
				continue
			p = 1.0 * num / photo_number
			h += - math.log(p)/math.log(2)*p
		return h
			
	def getRatioOfPeopleToPhoto(self):
		return 1.0 * self.getActualValue() / len(self._event['photos'])
		
	def getHistoricFeatures(self, entropy_para):
		# this method computes the features that capture the difference between current
		# event and background knowledge
		
		end_time = self.getLatestPhotoTime()
		begin_time = self.getEarliestPhotoTime()
		
		pi = PhotoInterface()
		pi.setDB('citybeat')
		pi.setCollection('photos')
		
		photos = []
		for day in xrange(1,15):
			# here 15 is hard coded because we use 14 days' data as the training
			et = end_time - day * 24 * 3600
			bt = begin_time - day * 24 * 3600
			day_photos = pi.rangeQuery(self._event['region'], [str(bt), str(et)])
			for photo in day_photos:
				# since rangeQuery sorts the photos from the most current to the most early
				# thus all the photos in the List "photos" are sorted by their created time from 
				# the most current to the most early
				photos.append(photo)
				
		
		
		event = Event()
		event.setPhotos(photos)
		event.setRegion(self._event['region'])
		event.setActualValue(event.getActualValueByCounting())
		event = EventFeature(event)
		
		cnt1 = self._getEntropy(entropy_para)
		cnt2 = event._getEntropy(entropy_para)
		enrtopy_delta = 0
		for i in xrange(entropy_para * entropy_para):
			dx = 1.0*cnt1[i]/self.getPhotoNumber() - 1.0*cnt2[i]/event.getPhotoNumber()
			enrtopy_delta += dx * dx
		enrtopy_delta = math.sqrt(enrtopy_delta)
		
		return [event.getAvgPhotoDis(), event.getTopWordPopularity(),
#		        event.getEntropy(entropy_para),
		        enrtopy_delta,
		        event.getAvgCaptionLen(), event.getRatioOfPeopleToPhoto()]
		
		

def generateData(biased=True):
	ei = EventInterface()
	ei.setDB('historic_alarm')
	ei.setCollection('labeled_event')
	events = ei.getAllDocuments()
	
	EventFeature.GenerateArffFileHeader()
	true_events = []
	false_events = []
	for event in events:
		event = EventFeature(event)
		feature_vector = event.extractFeatures(3)
		if feature_vector[-1] == 1:
			true_events.append(feature_vector)
		else:
			false_events.append(feature_vector)

	
	random.shuffle(false_events)
			
	for fv in true_events:
		for i in xrange(0, len(fv) - 1):
			print fv[i],',',
		print fv[-1]
		
	j = 0
	for fv in false_events:
		for i in xrange(0, len(fv) - 1):
			print fv[i],',',
		print fv[-1]
		j += 1
		if not biased and j == len(true_events):
			break

if __name__=='__main__':
	generateData()
#	ei = EventInterface()
#	ei.setDB('historic_alarm')
#	ei.setCollection('labeled_event')
#	event = ei.getDocument()
#	e = EventFeature(event)
#	e.getHistoricFeatures()