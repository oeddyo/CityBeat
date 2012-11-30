from instagram.client import InstagramAPI
#from lib.instagram_scan_storage import save_region_photos
from lib.mongo_storage import save_mogo
from lib.mysql_connect import add_table_region_photos
from lib.multithread import do_multithread_job

import Queue
import threading
import config
import time

import logging
logging.basicConfig(filename='./instagram.log', level=logging.DEBUG,
        format=' [%(asctime)s]   [%(levelname)s] (%(threadName)-10s) %(message)s '
        )

def do_func(para):
    mid_lat = para[0]
    mid_lng = para[1]
    period = para[2] 
    client = para[3] 
    radius_km = 0.38
    min_time = period[0]
    max_time = period[1]
    #try:
    res = client.media_search(lat = mid_lat, lng = mid_lng, max_timestamp = max_time, min_timestamp = min_time, return_json = True, distance = radius_km*1000, count=100)
    save_mogo(res, mid_lat, mid_lng)
    #except Exception as e:
    #    logging.warning(e)

sw_ne = (40.75953,-73.9863145)
periods = []
cur_time = int (time.time())
pre = cur_time
jobs = []
client = client = InstagramAPI(client_id =config.instagram_client_id, client_secret = config.instagram_client_secret)
while pre>=cur_time-10*3600:
    do_func( (40,30,(pre-60*3,pre),client))
    pre = pre-3*60
    #periods.append( (pre-3*60, pre) )