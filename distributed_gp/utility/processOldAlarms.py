from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface

def ProcessRawEvents(rawEvent):
	myDB = MongoDBInterface('grande', 27017)
	myDB.SetDB('citybeat')
	myDB.SetCollection('photos')
	
	event = {}
	photos = []
	lineNumber = -1
	for line in rawEvent:
		lineNumber = lineNumber + 1
		if lineNumber == 0:
			event['created_time'] = line.strip()
			continue
		if lineNumber == 1:
			event['lat'] = line.split(',')[0].strip()
			event['lng'] = line.split(',')[1].strip()
			continue
		if lineNumber == 2:
			vals = line.split(' ')
			event['predicted_mu'] = vals[0].strip()
			event['predicted_std'] = vals[1].strip()
			event['within_range'] = vals[4].strip()
			event['actual_value'] = vals[7].strip()
			continue
		photo_id = line.split(' ')[5].strip()
		photo = myDB.GetItem({'id':photo_id})
		photos.append(photo)
	event['photos'] = photos
	return event
		
		
	

def ReadAlarmsFromFile(fileName):
	file = open(fileName)
	
	adi = AlarmDataInterface('grande', 27017, 'historic_alarm', 'raw_event')
	mdbi = MongoDBInterface('grande', 27017)
	mdbi.SetDB('historic_alarm')
	mdbi.SetCollection('raw_event')
	
	event = []
	for line in file:
		if not line == '\n':
			event.append(line)
		else:
			if not event == []:
				print 'find an event'
				# in json
				processedEvent = ProcessRawEvents(event)
				merged = adi.MergeEvent(processedEvent)
				if not merged:
					mdbi.SaveItem(processedEvent)
				event = []


if __name__=="__main__":
	ReadAlarmsFromFile('alarm3_report.txt')
	