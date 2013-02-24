"""
    Given lantitude of the left-up corner of a city and the length of the city, scan the city every few minutes and store the data into db 
"""

from instagram.client import InstagramAPI
from lib.storage_interface import save_herenow
from lib.storage_interface import save_region_instagram
from lib.mysql_connect import add_table_pics_count
import Queue
import threading
import config
import time
from geopy import distance
import logging
logging.basicConfig(filename='./instagram.log', level=logging.DEBUG,
        format=' [%(asctime)s]   [%(levelname)s] (%(threadName)-10s) %(message)s '
        )

class ThreadUpdate(threading.Thread):
    def __init__(self, queue):
        self.client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)
        threading.Thread.__init__(self)
        self.queue = queue
        self.now = int(time.time())
        self.previous_time = int(time.time() - 15*60)
    def run(self):
        while True:
            job = self.queue.get()  #for each job, job[0] is the sw latitude, ne is the ne latitude
            mid_lat = (job[0][0] + job[1][0])*1.0/2
            mid_lng = (job[0][1] + job[1][1])*1.0/2
            time.sleep(1)
            radius_km = distance.distance( (mid_lat, mid_lng), (job[0][0], job[0][1])).km
            print radius_km
            logging.debug('mid is '+str(mid_lat)+","+str(mid_lng)+", r is "+str(radius_km))
            max_time = self.now
            counter = 0
            links_count = 0
            links = set()
            while True:
                counter+=1
                try:
                    res = self.client.media_search(lat = mid_lat, lng = mid_lng, max_timestamp = max_time, min_timestamp = self.previous_time, return_json = True, distance = radius_km*1000, count=100)
                except Exception as e:
                    logging.warning('Exception in instagram_scanner.py line 44. Error msg: %s'%e)
                    links_count = -1
                    break;
                print counter
                if len(res)==0 or max_time <= self.previous_time:
                    break
                else:
                    min_time = 100000000000;
                    for r in res:
                        min_time = min( int(r['created_time']), min_time)
                        links.add( r['link'] )
                        links_count+=1
                    if min_time<max_time:
                        max_time = min_time
                    else:
                        # in case all the pics in this interval are the same
                        max_time -= 60
                print 'next interval is ',self.previous_time, max_time
                #save_instagram_photo(page[0], mid_lat, mid_lng, radius_km)
                #counter += len(page[0])
            #save_instagram_region(counter, mid_lat, mid_lng, radius_km)
            real_links = -1
            if links_count==-1:
                real_links = -1
            else:
                real_links = len(links)
            region = [mid_lat, mid_lng, radius_km*1000, self.now + (self.now-self.previous_time)/2.0, real_links]
            save_region_instagram(region)
            
            print 'links',real_links
            print 'set links',len(links)
            print links
            logging.debug('for location '+str(mid_lat) + ','+str(mid_lng) +' the number is '+str(counter) +'\t'+str(len(links))+" links added")
            self.queue.task_done()

class instagramHeatUpdate:
    def __init__(self):
        pass 
    def execute(self, sw, ne):
        """given south-west lat&lng as well as north-east lat&lng, compute how we divide the map"""
        queue = Queue.Queue()
        fetched_dic = {}
        fetched_regions = []
        for i in range(3):
            t = ThreadUpdate(queue)
            t.setDaemon(True)
            t.start()
        n_regions = 25  #devide this region into 25*25 sub-regions
        lat_step = (ne[0]-sw[0])*1.0/n_regions
        lng_step = (ne[1]-sw[1])*1.0/n_regions
        
        cur_lat = sw[0]
        cur_lng = sw[1]
        
        #queue.put([(40.756496,-73.986856), (40.756596, -73.987856)])
        while cur_lat<ne[0]:
            while cur_lng<ne[1]:
                #print 'little region is ',cur_lat, cur_lng, 'to', cur_lat + lat_step, cur_lng+lng_step
                queue.put([(cur_lat, cur_lng), (cur_lat+lat_step, cur_lng+lng_step)] )
                cur_lng+=lng_step
            cur_lng = sw[1]
            cur_lat+=lat_step
        queue.join()

#add_table_herenow()
#add_table_herenow_region()
add_table_pics_count()
h = instagramHeatUpdate()
h.execute((40.698861,-74.051285), (40.811211,-73.88031))

