from instagram import InstagramAPI
import config
import time
from httplib2 import Http
clients = open('clients_list.csv').readlines()

count = 0
for line in clients:
    t = line.split()
    client = InstagramAPI( t[0], t[1])
    try:
        result = client.media_search(lat = 40.763381, lng = -73.954639 ,count=50, return_json = True, max_timestamp = 1361989315, min_timestamp=1361989315-600 )
    except Exception as e:
        print e
        print 'bad ',count
    count+=1
    
print time.time()
40.763381,-73.954639
