from datetime import datetime

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
		
	def getLocations(self):
		lat = float(self._tweet['location']['latitude'])
		lon = float(self._tweet['location']['longitude'])
		return [lat, lon]
		
	def getRawText(self):
		return self._tweet['text'].strip()
		
	def findKeywords(self, keywords):
		text = self.getRawText()
		occur = 0
		for word in keywords:
			if word in text:
				occur += 1
		return occur
	
	def getRetweetFreq(self):
		return int(self._tweet['retweet_count'])
		
def main():
	pass
	
if __name__ == '__main__':
	main()
		
	