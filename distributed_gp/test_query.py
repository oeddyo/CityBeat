


from utility.config import InstagramConfig
from  utility.photo_interface import PhotoInterface


start = 1365644367 - 14*3600*24
end = 1365644367

region = {'min_lat': 40.75419436, 'max_lng': -73.978088200000002, 'min_lng': -73.986094480000006, 'max_lat': 40.759499640000001}




pi = PhotoInterface()
pi.setDB('citybeat_production')
pi.setCollection('photos')
cursor = pi.rangeQuery(region, (str(start), str(end)))

cnt = 0
print 'here'

for p in cursor:
    cnt += 1
    print cnt
