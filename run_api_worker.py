from rq import Queue, Worker, Connection
from redis import Redis
import crawl_config

if __name__ == '__main__':
    redis_conn = Redis(crawl_config.redis_server)
    with Connection(connection=redis_conn):
        q = Queue() 
        Worker(q).work()
