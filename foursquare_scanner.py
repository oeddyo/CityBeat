"""
    Given lantitude of the left-up corner of a city and the length of the city, scan the city every few minutes and store the data into db 
"""

from instagram.client import InstagramAPI
import foursquare

from lib.storage_interface import save_herenow
from lib.storage_interface import save_region
from lib.mysql_connect import add_table_herenow
from lib.mysql_connect import add_table_herenow_region

import Queue
import threading

import config
import time

import logging
logging.basicConfig(filename='scan.log', level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
        )

class ThreadUpdate(threading.Thread):
    def __init__(self, queue, fetched_venues, fetched_regions):
        self.client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
        threading.Thread.__init__(self)
        self.queue = queue
        self.counter = 0
        self.fetched_venues = fetched_venues
        self.fetched_regions = fetched_regions
    def run(self):
        while True:
            job = self.queue.get()  #for each job, job[0] is the sw latitude, ne is the ne latitude
            mid_lat = (job[0][0] + job[1][0])*1.0/2
            mid_lng = (job[0][1] + job[1][1])*1.0/2
            time.sleep(1)
            sw = str(job[0][0])+','+str(job[0][1])
            ne = str(job[1][0])+','+str(job[1][1])
            lat_length = (job[1][0] - job[0][0])*1.0/2
            lng_length = (job[1][1] - job[0][1])*1.0/2
            #logging.debug('job is '+sw+" "+ne + ' and it is ' + str(self.counter)+'-th')
            logging.debug('mid is '+str(mid_lat)+","+str(mid_lng))
            res = self.client.venues.search(params={'sw':sw, 'ne':ne, 'limit':50, 'intent':'browse'})
            herenow_sum = 0
            for r in res['venues']:
                herenow_sum += r['hereNow']['count']
            region = [mid_lat, mid_lng, lat_length, lng_length, herenow_sum]
            self.fetched_regions.append( region ) 
            for venue in res['venues']:
                self.fetched_venues[venue['id']] = venue
            self.counter+=1
            self.queue.task_done()


class herenowUpdate:
    def __init__(self):
        pass 
    def execute(self, sw, ne):
        """given south-west lat&lng as well as north-east lat&lng, compute how we divide the map"""
        queue = Queue.Queue()
        fetched_dic = {}
        fetched_regions = []
        for i in range(10):
            t = ThreadUpdate(queue, fetched_dic, fetched_regions)
            t.setDaemon(True)
            t.start()
        n_regions = 25  #devide this region into 25*25 sub-regions
        
        lat_step = (ne[0]-sw[0])*1.0/n_regions
        lng_step = (ne[1]-sw[1])*1.0/n_regions
        
        cur_lat = sw[0]
        cur_lng = sw[1]

        while cur_lat<ne[0]:
            while cur_lng<ne[1]:
                #print 'little region is ',cur_lat, cur_lng, 'to', cur_lat + lat_step, cur_lng+lng_step
                queue.put([(cur_lat, cur_lng), (cur_lat+lat_step, cur_lng+lng_step)] )
                cur_lng+=lng_step
            cur_lng = sw[1]
            cur_lat+=lat_step
        
        queue.join()
        for v in fetched_dic.values():
            save_herenow(v)
        for r in fetched_regions:
            save_region(r)

add_table_herenow()
add_table_herenow_region()

h = herenowUpdate()
h.execute((40.698861,-74.051285), (40.811211,-73.88031))

