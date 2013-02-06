import time
import csv
import sys

import pymongo
from pymongo import Connection
from pymongo.database import Database


connection = Connection( 'grande')
db = Database(connection, "citybeat")


id = set()
for photo in db.photos.find():
    if int(photo['created_time']) > 1354320000:
        continue
    if photo['id'] in id:
        continue
    id.add(photo['id'])
    print "%s,%s,%s,%s,%s,%s,%s"%(photo['location']['latitude'],photo['location']['longitude'],photo['user']['username'],photo['user']['id'],photo['filter'],photo['link'],photo['images']['standard_resolution']['url'])



