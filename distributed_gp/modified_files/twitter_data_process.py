import pymongo
import pandas as pd
from pandas import Series
from datetime import datetime
import calendar

def find_tweets_given_region(lat, lng, resample_freq, db_name, count_people = True):
    mongo = pymongo.Connection("grande", 27017)
    mongo_db = mongo[db_name]
    mongo_collection = mongo_db.tweets
    dates = []
    counts = []
    seen = set()
    pre_date = {}       #for a single user, when is his last photo; this is used to avoid to count a user's taking many pics in a row
    tweets = []
    
    for p in mongo_collection.find({"mid_lat":float(lat), "mid_lng":float(lng)}):
        if p['id'] in seen:
            continue
        seen.add(p['id'])
        tweets.append( p )
    
    tweets = sorted(tweets, key = lambda x: x['created_at'])
    
    tweets_return = []
    for tweet in tweets:
        dt = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        dt = calendar.timegm(dt.utctimetuple())
        if count_people:
            user = tweet['user']['screen_name'] 
            if user not in pre_date:
                pre_date[user] = dt
                tweets_return.append( p )
                dates.append(datetime.utcfromtimestamp(dt))
                #float(p['created_at'])))
                counts.append(1)
            else:
                if float(dt) - float(pre_date[user]) >600:        # within 10 minutes count it as a single user
                    pre_date[user] = dt
                    tweets_return.append( p )
                    dates.append(datetime.utcfromtimestamp(dt))
                    counts.append(1)
                else:
                    #print 'pre is ',datetime.utcfromtimestamp(float(pre_date[user])),' next is ',datetime.utcfromtimestamp(float(p['created_time']))
                    continue
        else: 
            dates.append(datetime.utcfromtimestamp(float(dt)))
            counts.append(1)
            tweets_return.append(p)
    """ 
    for p in photos_return:
        print p['created_time'] , p['user']['username'], p['link']
    print '\n\n'
    """
    ts = Series(counts, index = dates)
    ts = ts.resample(resample_freq,how='sum', label='right')
    print ts
    return ts, tweets_return

find_tweets_given_region(40.750542,-73.9863145, '10Min', 'tweets', True)

"for each mid_lat, mid_lng, read all the photos from there"
"organize it in pandas and add it into the job queue"




