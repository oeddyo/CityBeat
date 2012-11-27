"""
Download all the plazas metas for all the ids in plazas
"""

from mysql_connect import connect_to_mysql

import logging
import Queue
import threading


class ThreadDownload(threading.Thread):
    def __init__(self, queue, do_func, logfile):
        threading.Thread.__init__(self)
        self.queue = queue
        self.do_func = do_func
        logging.basicConfig(filename=logfile, level=logging.DEBUG,
        format=' [%(asctime)s]   [%(levelname)s] (%(threadName)-10s) %(message)s '
        )
    def run(self):
        while True:
            try:
                job = self.queue.get()
                self.do_func( job )
            except Exception as e:
                logging.debug('Exception msg: %s',e)
            finally:
                self.queue.task_done()

def do_multithread_job(do_func, jobs, n_thread = 10, logfile = './download.log'):
    """
    Do multithreading work. Parameters,
    do_func - user specified function which is actually doing the work. 
    jobs - the jobs do_func should finish
    n_thread - number of thread to do the works
    logfile - where should the log file be put
    """
    queue = Queue.Queue()
    for i in range(n_thread):
        t = ThreadDownload(queue,  do_func, logfile)
        t.setDaemon(True)
        t.start()
    for id in jobs:
        queue.put(id)
    queue.join()


"""
def do_work(venue_id):
    meta_data = download_meta_data(venue_id)
    save_venue_meta(meta_data, table = 'plazas_meta')

def main():
    sql = "select id from plazas"
    cursor = connect_to_mysql()
    cursor.execute(sql)
    
    ids = []
    count = 10
    for r in cursor.fetchall():
        ids.append(r['id'])
        count-=1;
        if(count<=0):break
    multithread_download(do_work, ids, 10, './heihei.log')
main()
"""
