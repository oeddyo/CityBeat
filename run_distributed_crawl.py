import os
from rq import Queue, Connection
from instagram.client import InstagramAPI
from worker_download import download
from redis import Redis
import time
from random import randrange

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
    return ll_pairs

def main():
    ll_pairs = get_freq()
    cur_time =  int (time.time())
    clients = get_client_list()
    redis_conn = Redis('bwi')
    q = Queue(connection=redis_conn)
    
    for location in ll_pairs:
        pre = cur_time
        while pre>cur_time - 14*3600*24:
            client = clients[randrange(len(clients))]
            paras = ( location[0], location[1],(pre-location[2],pre), client)
            pre -= location[2]
            q.enqueue_call(func=download,args=(paras,),timeout=360000)
    
    """
    periods = []
    cur_time = int (time.time())

    client_pairs = [get_client(('4d9231b411eb4ef69435b40eb83999d6','204c565fa1244437b9034921e034bdd6')), 
    #client_pairs = [get_client(('5264cb2c127c45bca1384f5b5a0d426d','196e23c473cf4ac6b66508d4607bbd27')), 
            get_client(('57e751d0bf864cf09364938a4417104a','df1dd54df83d405c9f7a8ffa37ccd029'))]
    
    pre = cur_time
    job_count = 0
    res = {}

    while pre>cur_time - 10*3600*24:
        os.system('clear')
        if job_count%2 == 0:
            client = client_pairs[0]
        else:
            client = client_pairs[1]
        paras = (sw_ne[0], sw_ne[1], (pre-2*60, pre), client,)
        pre-=2*60
        res[job_count] = q.enqueue_call(func=download, args=(paras,),timeout=360000)
        job_count+=1

    done = False
    failed_job = 0
    count = 0
    while not done:
        os.system('clear')
        print '%d jobs completed, %d jobs failed!'%(count, failed_job)
        done = True
        count = 0
        for x in range(job_count):
            r = res[x].return_value
            if r == False:
                print 'Job fail'
                failed_job += 1
            if r is None:
                done = False
            elif r==True:
                count += 1
        time.sleep(0.2)
"""
if __name__== '__main__':
    with Connection():
        main()
