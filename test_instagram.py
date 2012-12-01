from instagram import InstagramAPI
import config
import time
client = InstagramAPI( '57e751d0bf864cf09364938a4417104a', 'df1dd54df83d405c9f7a8ffa37ccd029')
print time.time()
40.763381,-73.954639
result = client.media_search(lat = 40.763381, lng = -73.954639 ,count=100, return_json = True)
print result
print len(result)
