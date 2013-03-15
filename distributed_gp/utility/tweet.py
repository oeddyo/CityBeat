from datetime import datetime

from tweet_interface import TweetInterface

from datetime import datetime, timedelta, date
from email.utils import parsedate_tz

import calendar


import operator
import string
import types
import time

class Tweet(object):
	
	def __init__(self, tweet=None):
		# the input argument event should be a json, dictionary
		if not tweet is None:
			if type(tweet) is types.DictType:
				self._tweet = tweet
			else:
				self._tweet = tweet.toJSON()
	
	def getCreatedUTCTimestamp(self):
		ts = self._tweet['created_at']
		dt = calendar.timegm(parsedate_tz(ts.strip()))
		return str(dt)
	
	def toJSON(self):
		# return a dict, not json
		return self._tweet
		
	def getGeolocation(self):
		pass
		
	def getRawText(self):
		return self._tweet['text']
		
def main():
	ti = TweetInterface()
	tweet_cur = ti.getAllDocuments()
	for tweet in tweet_cur:
		tweet = Tweet(tweet)
	
if __name__ == '__main__':
	main()
		
	