from tweet_interface import TweetInterface
from event_feature import EventFeature
from tweet import Tweet
from event_interface import EventInterface
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from tweet_cluster import TweetCluster


import kl_divergence as KLDivergence

import operator
import string
import types
import random
import math
import numpy

class EventFeatureTwitter(EventFeature):
	
	def extractFeatures(self, entropy_para=3, k_topwords=3):
		# it outputs the feature vector
		self.preprocess()
		avg_cap_len = self.getAvgCaptionLen()
		dis_feautures = self.getPhotoDisFeatures()
		min_photo_dis = dis_feautures[0]
		max_photo_dis = dis_feautures[1]
		std_photo_dis = dis_feautures[2]
		avg_photo_dis = dis_feautures[3]
		median_photo_dis = dis_feautures[4]
		cap_dis_features = self.getPhotoCaptionDisFeatures()
		min_photo_dis_cap = cap_dis_features[0]
		max_photo_dis_cap = cap_dis_features[1]
		std_photo_dis_cap = cap_dis_features[2]
		mean_photo_dis_cap = cap_dis_features[3]
		median_photo_dis_cap = cap_dis_features[4]
		cap_per = self.getCaptionPercentage()
		std = self.getPredictedStd()
		top_word_pop = self.getTopWordPopularity(k_topwords)
		zscore = self.getZscore()
		entropy = self.getEntropy(entropy_para)
		
		label = int(self.getLabel())
		event_id = str(self._event['_id'])
		
		tfidf_top3 = self.getTopWordByTFIDF(3)
		res = self.countHashtagsFromPhotosContainingTopKeywords(3)
		hashtage_cnt3 = res[0]
		number_photos_associated_with_keywords3 = res[1]
		
		
		
#		historic_features = [0]*3  # for test only
		historic_features = self.getHistoricFeatures(entropy_para)
		diff_avg_photo_dis = avg_photo_dis - historic_features[0]
		diff_top_word_pop = historic_features[1]
		diff_entropy = historic_features[2]
		
		location_name_similarity = self.getTopPhotosLocationSimilarity()
#		location_name_same = self.checkIfTopPhotoLocationSame()
		
		return [avg_cap_len,
		        min_photo_dis, max_photo_dis, std_photo_dis, avg_photo_dis, median_photo_dis,
		        min_photo_dis_cap, max_photo_dis_cap,	std_photo_dis_cap,
		        mean_photo_dis_cap, median_photo_dis_cap,
		        cap_per,
		        std, top_word_pop, zscore, entropy, #ratio,
		        diff_avg_photo_dis, diff_top_word_pop, diff_entropy,
		        tfidf_top3[0], tfidf_top3[1], tfidf_top3[2], 
		        hashtage_cnt3[0], hashtage_cnt3[1], hashtage_cnt3[2],
		        number_photos_associated_with_keywords3[0], number_photos_associated_with_keywords3[1], number_photos_associated_with_keywords3[2],
		        location_name_similarity, 
#		        location_name_same,
		        event_id,
		        label]
		        
	def printFeatures(self):
		feature_list = self.extractFeatures()
		n = len(feature_list)
		for i in xrange(0, n-1):
			print feature_list[i],',',
		print feature_list[-1]
			
			
#	@staticmethod
	def GenerateArffFileHeader(self):
		print '@relation CityBeatEvents'
		print '@attribute AvgCaptionLen real'
		print '@attribute stat_MinPhotoDis real'
		print '@attribute stat_MaxPhotoDis real'
		print '@attribute stat_StdPhotoDis real'
		print '@attribute AvgPhotoDis real'
		print '@attribute stat_MedianPhotoDis real'
		print '@attribute stat_MinPhotoDisbyCap real'
		print '@attribute stat_MaxPhotoDisbyCap real'
		print '@attribute stat_StdPhotoDisbyCap real'
		print '@attribute MeanPhotoDisbyCap real'
		print '@attribute stat_MedianPhotoDisbyCap real'
		print '@attribute CaptionPercentage real'
		print '@attribute PredictedStd real'
		print '@attribute TopWordPopularity real'
		print '@attribute Zscore real'
		print '@attribute Entropy real'
		print '@attribute diff_AvgPhotoDis real'
		print '@attribute diff_TopWordPopularity real'
		print '@attribute diff_Entropy real'

		print '@attribute tfidf1 real'	
		print '@attribute tfidf2 real'	
		print '@attribute tfidf3 real'
		
		print '@attribute NumberOfHashtages1 real'	
		print '@attribute NumberOfHashtages2 real'	
		print '@attribute NumberOfHashtages3 real'	
		
		print '@attribute NumberOfPhotsoContaingTopWord1 real'
		print '@attribute NumberOfPhotsoContaingTopWord2 real'
		print '@attribute NumberOfPhotsoContaingTopWord3 real'
		
		print '@attribute Top10PhotoLocationNameFreq real'
#		print '@attribute Top3PhotoLocationNameSame real'
								
		print '@attribute ID string'
		print '@attribute label {1,-1}'
		print '@data'
		
	def extractFeatureFromTweet(self, keyword_num=4):
		tc = TweetCluster()
		tc.setRegion(self._event['region'])
		#tc.setPeriod([str(self.getEarliestPhotoTime()), str(self.getLatestPhotoTime())])
		tc.getTweetFromRangeQuery()
		
		keywords_pop = self._getTopWords(keyword_num, stopword_removal=True)
		keywords = []
		for word, freq in keywords_pop:
			keywords.append(word)
		print tc.getNumberOfTweets()
		per = tc.computePercentageOfTweetWithKeyword(keywords, 1)
		diff_per = tc.computeDifferenceComparedWithHistoricPercentageOfTweetWithKeyword(keywords, 1)
#		print per, diff_per
		return per, diff_per

if __name__=='__main__':
	generateData()
#	ei = EventInterface()
#	ei.setDB('historic_alarm')
#	ei.setCollection('labeled_event')
#	event = ei.getDocument()
#	e = EventFeature(event)
#	e.getHistoricFeatures()