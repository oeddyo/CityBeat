from rq import Queue, Connection
from instagram.client import InstagramAPI
from worker_download import download
from random import randrange
from crawl_config import redis_server
from redis import Redis
import calendar
from datetime import datetime
import sys
import time
import os

def get_client(client_pair):
    return InstagramAPI(client_id = client_pair[0], client_secret = client_pair[1])

def get_client_list():
    lines = open('./clients_list.csv','r').readlines()
    c_list = []
    for line in lines:
        t = line.split()
        c_list.append(get_client((t[0],t[1])))
    return c_list

def get_freq():
    lines = open('./number.csv','r').readlines()
    ll_pairs = []
    for line in lines:
        t = line.split(',')
        num = float(t[2])
        freq = 60.0/(num/20.0)
        ll_pairs.append( (t[0],t[1],int( freq*60 )))
    ll_pairs.reverse()
    return ll_pairs

def main():
    """parse parameter here"""
    
    if len(sys.argv)==3:
        start_utc_timestamp = int(calendar.timegm( datetime.utcnow().utctimetuple() ))
        seconds_to_traceback = int(sys.argv[1])
        mongo_db_name = sys.argv[2]
    elif len(sys.argv)==4:
        start_utc_timestamp = int(sys.argv[1])
        seconds_to_traceback = int(sys.argv[2])
        mongo_db_name = sys.argv[3]
    else:
        sys.stderr.write("Usage: python %s (start_utc_timestamp) seconds_to_traceback mongo_db_name"%sys.argv[0])
        raise SystemExit(1)


    #if len(sys.argv)!=4:
    #    sys.stderr.write("Usage: python %s start_utc_timestamp seconds_to_traceback mongo_db_name"%sys.argv[0])
    #    raise SystemExit(1)
    #start_utc_timestamp = int(sys.argv[1])
    #seconds_to_traceback = int(sys.argv[2])
    #mongo_db_name = sys.argv[3]
    
    ll_pairs = get_freq()
    print ll_pairs
    cur_time =  start_utc_timestamp
    clients = get_client_list()
    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)
    api_assign_count = 0   
    counts = [0]*len(clients) 
    for location in ll_pairs:
        pre = cur_time
        print 'assign count ',api_assign_count
        while pre > cur_time - seconds_to_traceback:
            client = clients[randrange(len(clients))]
            counts[randrange(len(clients))]+=1
            time_window = int(location[2])
            #if int(location[2])<600:
                #time_window = int (((int (location[2])))*1.0/2)
            #    time_window = int(time_window/1.5)
            hour = datetime.fromtimestamp(pre).hour
            #if hour>=1 and hour<=10:
            #    time_window = time_window*3
            paras = ( location[0], location[1],(pre-time_window,pre), client, mongo_db_name)
            pre -= time_window
            q.enqueue_call(func=download,args=(paras,),timeout=572000)
            api_assign_count+=1
    print counts


if __name__=='__main__':
    main()
