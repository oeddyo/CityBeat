from config import InstagramConfig
from photo_interface import PhotoInterface

class Region:
	
	def __init__(self, coordinates):
		# coordinates must be formatted as [min_lat, min_lng, max_lat, max_lng]
		self.min_lat = coordinates[0]
		self.min_lng = coordinates[1]
		self.max_lat = coordinates[2]
		self.max_lng = coordinates[3]
			
	def _insideRegion(self, coordinate):
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
		pi = PhotoInterface()
		
		cnt = {}
		s = 0
		for region in region_list:
			cnt[region] = 0
			photos = pi.rangeQuery(region)
			tmp_cnt = photos.count()
			cnt[region] = tmp_cnt
			region.display()
			print tmp_cnt
			s += tmp_cnt
		print s
		

if __name__=="__main__":
	coordinates = [InstagramConfig.photo_min_lat, InstagramConfig.photo_min_lng,
	               InstagramConfig.photo_max_lat, InstagramConfig.photo_max_lng]
	nyc = Region(coordinates)
	pi = PhotoInterface()
	pi.rangeQuery(nyc)
	region_list = nyc.divideRegions(InstagramConfig.region_N, InstagramConfig.region_M)
	nyc.filterRegion(region_list)