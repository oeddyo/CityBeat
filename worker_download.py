from instagram.client import InstagramAPI
from lib.mongo_storage import save_mogo

import config
import time

"""
import logging
logging.basicConfig(filename='./instagram.log', level=logging.DEBUG,
        format=' [%(asctime)s]   [%(levelname)s] (%(threadName)-10s) %(message)s '
        )
"""
def download(para):
    print para
    mid_lat = para[0]
    mid_lng = para[1]
    period = para[2] 
    client = para[3] 
    db_name = para[4]
    radius_m = 400
    min_time = period[0]
    max_time = period[1]
    #try
    res = client.media_search(lat = mid_lat, lng = mid_lng, max_timestamp = max_time, min_timestamp = min_time, return_json = True, distance = radius_m, count=60)
        #print len(res)
    save_mogo(res, mid_lat, mid_lng, db_name)
    time.sleep(0.35)
    #except Exception as e:
    #    print 'Error info',e
    #    return False
        #logging.warning(e)
    return True

