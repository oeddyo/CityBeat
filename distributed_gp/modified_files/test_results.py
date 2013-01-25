from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface


def QueryFromDB():
	mdbi = MongoDBInterface('grande', 27017)
	mdbi.SetDB('historic_alarm')
	mdbi.SetCollection('raw_event')
	
	lat = '40.750542'
	lng = '-73.9931535'
	conditions = {'lat':lat, 'lng':lng}
	events = mdbi.GetAllItems(conditions)
	i = 0
	numberOfPhotos = []
	for event in events:
		i = i + 1
		numberOfPhotos.append(len(event['photos']))
		print len(event['photos'])
		print event['created_time']


def main():
	QueryFromDB()

if __name__ == '__main__':
	main()
	