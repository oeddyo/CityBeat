import operator

from config import InstagramConfig
from photo_interface import PhotoInterface
from mongodb_interface import MongoDBInterface

class Region:
	
	def __init__(self, coordinates):
		# coordinates must be formatted as [min_lat, min_lng, max_lat, max_lng]
		self.min_lat = coordinates[0]
		self.min_lng = coordinates[1]
		self.max_lat = coordinates[2]
		self.max_lng = coordinates[3]
			
	def insideRegion(self, coordinate):
		# coordinates must be formatted as [lat, lng]
		lat = coordinate[0]
		lng = coordinate[1]
		if self.min_lat > lat or lat > self.max_lat:
			return False
		if self.min_lng > lng or lng > self.max_lng:
			return False
		return True
		
	def display(self):
		print [self.min_lat, self.min_lng, self.max_lat, self.max_lng]
		
	def getMidCoordinates(self):
		return [(self.min_lat + self.max_lat)/2, (self.min_lng + self.max_lng)/2]
		
	def divideRegions(self, n, m):
		# this method only works when the "region" is the whole region
		# divde the whole NYC into n*m rectangular regions
		lat_offset = 	(self.max_lat - self.min_lat) / n
		lng_offset = 	(self.max_lng - self.min_lng) / m
		region_list = []
		for i in xrange(0, n):
			low_lat = self.min_lat + i * lat_offset
			high_lat = low_lat + lat_offset
			for j in xrange(0, m):
				low_lng = self.min_lng + j * lng_offset
				high_lng = low_lng + lng_offset
				coordinates = [low_lat, low_lng, high_lat, high_lng]
				r = Region(coordinates)
				region_list.append(r)
		return region_list
	
	def filterRegion(self, region_list):
		
		end_time = 1359704845 - 7*3600*24
		begin_time = end_time - 14*3600*24
		pi = PhotoInterface()
		photos = pi.rangeQuery(period=[str(begin_time), str(end_time)])
		region_number = len(region_list)
		number_photo_in_region = [0]*region_number
		p = 0
		for photo in photos:
			p += 1
			if p % 10000 == 0:
				print p
			lat = float(photo['location']['latitude'])
			lng = float(photo['location']['longitude'])
			flag = 0
			for i in xrange(region_number):
				if region_list[i].insideRegion([lat, lng]):
					number_photo_in_region[i] += 1
					flag = 1
					break
			if flag == 0:
				print 'bad photo:',photo
		
		region_tuples = []
		for i in xrange(0, region_number):
			region_tuples.append([region_list[i], number_photo_in_region[i]])
		
		region_tuples.sort(key=operator.itemgetter(1), reverse=True)
		
		print region_tuples
		
		valid_region_number = int(0.5 + 1.0 * region_number * InstagramConfig.region_percentage)
		valid_regions = []
		for i in xrange(0, valid_region_number):
			valid_regions.append(region_tuples[i])
		
		print region_tuples
		

if __name__=="__main__":
	coordinates = [InstagramConfig.photo_min_lat, InstagramConfig.photo_min_lng,
	               InstagramConfig.photo_max_lat, InstagramConfig.photo_max_lng]
	nyc = Region(coordinates)
	pi = PhotoInterface()
	pi.rangeQuery(nyc)
	region_list = nyc.divideRegions(InstagramConfig.region_N, InstagramConfig.region_M)
	nyc.filterRegion(region_list)