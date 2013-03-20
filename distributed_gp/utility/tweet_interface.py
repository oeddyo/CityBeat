##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A high level interface to access the alarm data, for labeling the event
##########
#Edited by: (Please write your name here)#

from mongodb_interface import MongoDBInterface
from event import Event
from tweet import Tweet
from config import TwitterConfig
from datetime import datetime
from bson.objectid import ObjectId


import config
import time
import logging
import string
import types
import json

class TweetInterface(MongoDBInterface):
	
	def __init__(self, db=TwitterConfig.tweet_db,  
	             collection=TwitterConfig.tweet_collection):
	  # initialize an interface for accessing event from mongodb
	  super(TweetInterface, self).__init__()
	  self.setDB(db)
	  self.setCollection(collection)
	  
	def saveDocument(self, tweet):
		if not type(tweet) is types.DictType:
			tweet = tweet.toJSON()
		if 'location' not in tweet.keys():
			if 'geo' not in tweet.keys():
				return
			location = {}
			location['latitude'] = tweet['geo']['coordinates'][0]
			location['longitude'] = tweet['geo']['coordinates'][1]
			tweet['location'] = location
		
		tweet['created_time'] = Tweet(tweet).getCreatedUTCTimestamp()
		
		super(TweetInterface, self).saveDocument(tweet)
	
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
			period_conditions = {'created_time':{'$gte':str(period[0]), '$lte':str(period[1])}}

		conditions = dict(region_conditions, **period_conditions)
		
		#returns a cursor
		#sort the tweet in chronologically decreasing order
		return self.getAllDocuments(conditions).sort('created_time', -1)
	  
def main():
	
	ti = TweetInterface()
#	period = ['1353641910', '1355641910']
#	region = {'min_lat':-74, 'max_lat':-73, 'min_lng':40, 'max_lng':41}
#	print ti.rangeQuery(region=region, period=period).count()
		
	fid = open('nyc_tweets.txt')
	for line in fid:
		tweet = json.loads(line.strip())
		ti.saveDocument(tweet)
	fid.close()
	
#	ti = TweetInterface()
#	tweet = ti.getDocument()
#	for tweet in tweets:
#		tweet = Tweet(tweet)
##		retweet = tweet.getRetweetFreq()
##		if retweet > 0:
##			print retweet
#		keywords = ['game', 'knicks']
#		if tweet.findKeywords(keywords) == len(keywords):
#			print tweet.getRawText().
#			print 

			
if __name__ == '__main__':
	main()