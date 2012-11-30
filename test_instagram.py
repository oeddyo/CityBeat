from instagram import InstagramAPI
import config
import time
client = InstagramAPI( '4d9231b411eb4ef69435b40eb83999d6', '204c565fa1244437b9034921e034bdd6')
print time.time()
40.763381,-73.954639
result = client.media_search(lat = 40.763381, lng = -73.954639 ,count=100, return_json = True)
print type(result[0])
print len(result)
