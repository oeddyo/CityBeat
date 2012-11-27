"""
    Given lantitude of the left-up corner of a city and the length of the city, scan the city every few minutes and store the data into db 
"""

from instagram.client import InstagramAPI
from lib.instagram_scan_storage import save_region_photos
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
    print para
    #mid_lat = (sw_ne[0][0] + sw_ne[1][0])*1.0/2
    #mid_lng = (sw_ne[0][1] + sw_ne[1][1])*1.0/2
    #radius_km = distance.distance( (mid_lat, mid_lng), (job[0][0], job[0][1])).km
    radius_km = 0.38
    logging.debug('mid is '+str(mid_lat)+","+str(mid_lng)+", r is "+str(radius_km))
    min_time = period[0]
    max_time = period[1]
    try:
        res = client.media_search(lat = mid_lat, lng = mid_lng, max_timestamp = max_time, min_timestamp = min_time, return_json = False, distance = radius_km*1000, count=100)
        save_region_photos(res, mid_lat, mid_lng)
    except Exception as e:
        print 'Exception!'
        logging.warning('{par:{%s,%s}, msg:{%s}}'%(str(sw_ne),str(period),e))


def main():
    add_table_region_photos()
    cur_time = int (time.time() )
    sw_ne = (40.773012,-73.9863145)
    
    periods = []
    pre = cur_time
    jobs = []
    client = client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)
    while pre>=cur_time-10*3600*24:
        periods.append( (pre-10*60, pre) )
        jobs.append( (sw_ne[0], sw_ne[1], (pre-10*60,pre), client) ) 
        pre-=60*10
    do_multithread_job(do_func, jobs, 5, './test_multi_insta_scan.log')
    

main()
