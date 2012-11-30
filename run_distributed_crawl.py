import os
from rq import Queue, Connection
from instagram.client import InstagramAPI
from worker_download import download
from redis import Redis
import time

def get_client(client_pair):
    return InstagramAPI(client_id = client_pair[0], client_secret = client_pair[1])

def main():
    sw_ne = (40.75953,-73.9863145)
    periods = []
    cur_time = int (time.time())

    client_pairs = [get_client(('57e751d0bf864cf09364938a4417104a','196e23c473cf4ac6b66508d4607bbd27')), 
            get_client(('57e751d0bf864cf09364938a4417104a','df1dd54df83d405c9f7a8ffa37ccd029'))]
    

    pre = cur_time
    job_count = 0
    redis_conn = Redis('bwi')
    q = Queue(connection=redis_conn)
    res = {}

    while pre>cur_time - 10*3600*24:
        os.system('clear')
        if job_count%2 == 0:
            client = client_pairs[0]
        else:
            client = client_pairs[1]
        paras = (sw_ne[0], sw_ne[1], (pre-5*60, pre), client)
        pre-=5*60
        res[job_count] = q.enqueue(download, paras)
        job_count+=1

    done = False
    while not done:
        os.system('clear')
        done = True
        count = 0
        for x in range(job_count):
            r = res[x].return_value
            if r is None:
                done = False
            else:
                count+=1
        print '%d jobs completed!'
        time.sleep(0.2)

if __name__== '__main__':
    with Connection():
        main()
