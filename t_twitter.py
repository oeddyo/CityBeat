import datetime
import tweepy
from tweepy.error import TweepError
from tweepy.parsers import RawJsonParser
import json
import time
import sys

import pymongo

def tweepy_auth():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_KEY = ''
    ACCESS_SECRET = ''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    #api = tweepy.API(auth)
    return auth


#tweepy parser
class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, db_name):
        tweepy.StreamListener.__init__(self)
        print 'ok'
    def on_status(self, status):
        print "should start here"
        print dir(status)
        print "should end here"
        print "%s\t%s\t%s\t%s\t%s" % (
                status.text,
                status.author.screen_name, 
                status.created_at, 
                status.source,
                status.lang
                )
        return True
        def on_error(self, status_code):
            print >> sys.stderr, 'Encountered error with status code:', status_code
            return True # Don't kill the stream
        def on_timeout(self):
            print >> sys.stderr, 'Timeout...'
            return True # Don't kill the stream


def main2():
    auth = tweepy_auth()
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener('tweets'), timeout=60)
    streaming_api.filter(follow=None ,locations =[26.273714,-125.771484, 48.107431,-61.171875])
        
        
    #streaming_api.filter(follow=None , track=[ 'I feel lonely','I am feeling lonely', "I'm feeling lonely", "I am lonely", "I'm lonely", "I am so lonely", "I'm so lonely", "I feel so lonely", "I feel very lonely", "I am very lonely", "I'm very lonely", "I feel alone", "I feel very alone", "I feel so alone", "I'm feeling alone", "I'm feeling very alone", "I'm feeling so alone", "I feel left out", "I am feeling left out", "I'm feeling left out", "I feel isolated",   "I am feeling isolated", "I'm feeling isolated"])
    #, locations =[26.273714,-125.771484, 48.107431,-61.171875])
    print 'ends'

if __name__=="__main__":
    main2()
