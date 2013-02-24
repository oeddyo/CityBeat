import datetime
import tweepy
from tweepy.error import TweepError
from tweepy.parsers import RawJsonParser
import json
import time
import sys

import pymongo

def tweepy_auth():
    CONSUMER_KEY = '01gugiESt8CSq97ypjTQg'
    CONSUMER_SECRET = 'JQPPGBxZploR3fG9TDylDH3ZrjJgcHlsLSR5SSBY'
    ACCESS_KEY = '3183721-QQZ4rpf5cv3og207hSwHFPGpsTf5v7kPuY6MO9S9iY'
    ACCESS_SECRET = '2DP9FW6ZmCis4TewZLYHQGbqWiThq4uQqSQbJSiFJw'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    #api = tweepy.API(auth)
    return auth


#tweepy parser
import tweepy
import json
 
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
             
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, db_name):
        tweepy.StreamListener.__init__(self)
        self.mid_list = []
        self.db_name = db_name
        lines = open('number.csv').readlines()
        self.mid_list = [(mid.split(',')[0], mid.split(',')[1]) for mid in lines ]
    def save_to_mongo(self,tweet):
        tweet = json.loads(tweet.json)
        if tweet['coordinates'] is None:
            return
        mongo = pymongo.Connection("grande",27017)
        mongo_db = mongo[self.db_name]
        mongo_collection = mongo_db.tweets

        #find closest mid point as mid_lat, mid_lng
        t_min = 999999999
        mid_lat = -1
        mid_lng = -1
        for p in self.mid_list:
            m_lat = float(p[0])
            m_lng = float(p[1])
            lat = tweet['coordinates']['coordinates'][1]
            lng = tweet['coordinates']['coordinates'][0]
            dis = (lat-m_lat)*(lat-m_lat) + (lng-m_lng)*(lng-m_lng)
            if dis<t_min:
                t_min = dis
                mid_lat = m_lat
                mid_lng = m_lng
        tweet['mid_lat'] = mid_lat
        tweet['mid_lng'] = mid_lng
        tweet['_id'] = tweet['id']
        mongo_collection.save(tweet)


    def on_status(self, status):
        try:
            print "%s\t%s\t%s\t%s\t%s" % (status.text, 
                    status.author.screen_name, 
                    status.created_at, 
                    status.source,
                    status.coordinates['coordinates']
                    )
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass
        def on_error(self, status_code):
            print >> sys.stderr, 'Encountered error with status code:', status_code
            return True # Don't kill the stream
        def on_timeout(self):
            print >> sys.stderr, 'Timeout...'
            return True # Don't kill the stream


def main2():
    auth = tweepy_auth()
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener('tweets'), timeout=60)
    streaming_api.filter(follow=None, track='good')
           

if __name__=="__main__":
    main2()


def main():
    api = tweepy.API(parser=RawJsonParser())
    api = tweepy.API()
    rets = api.search(q=' ',count=100,geocode="40.719084,-73.9931535,0.38mi")
     
    max_id = rets.max_id
    print max_id

    try:
        for page in tweepy.Cursor(api.search, q ="new", rpp=100, max_id = max_id , geocode="40.719084,-73.9931535,0.38mi").pages():
            print len(page)
            print page[0].created_at
            for p in page:
                if p.text.find("I'm at")==-1 and p.geo is not None:
                    print p.created_at, p.geo,p.text
            time.sleep(3)
    except TweepError, reason:
        print reason
    except TypeError, reason:
        print reason


    #json_rets =  json.loads(rets)
    #print len(json_rets)

