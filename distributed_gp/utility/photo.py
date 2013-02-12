import types


class Photo:
	# before you save an instance of Photo, convert it to JSON first
	# by photo.toJSON()
	
	def __init__(self, photo):
		# One must input a photo as an instance of json or class Photo
		if type(photo) is types.DictType:
			self._photo = photo
		else:
			self._photo = photo.toJSON()
	
	def getLocations(self):
		lat = float(self._photo['location']['latitude'])
		lon = float(self._photo['location']['longitude'])
		return [lat, lon]
	
	def getUserName(self):
		return self._photo['user']['username']
		
	def getCaption(self):
		if self._photo['caption'] is None:
			return ''
		if self._photo['caption']['text'] is None:
			return ''
		return self._photo['caption']['text']
	
	def toJSON(self):
		return self._photo
	
	def equalWith(self, photo):
		return self.compare(photo) == 0
	
	def compare(self, photo):
		if not type(photo) is types.DictType:
			photo = photo.toJSON()
		t1 = int(self._photo['created_time'])
		t2 = int(photo['created_time'])
		id1 = str(self._photo['id'])
		id2 = str(photo['id'])
		
		if t1 > t2:
			return 1
		if t1 < t2:
			return -1
		if id1 > id2:
			return 1
		if id1 < id2:
			return -1
		return 0
	
	def _delUnrelatedFields(self):
		# this method is only used for frontend
#		['caption']['from']
#['comments']
#['filter']
#['user']
#['images']['low_resolution']
#['images']['standard_resolution']
		if self._photo['caption'] is not None:
			if self._photo['caption']['from'] is not None:
				del self._photo['caption']['from']
		if self._photo['filter'] is not None:
			del self._photo['filter']
		if self._photo['user'] is not None:
			del self._photo['user']
		if self._photo['images'] is not None:
			if self._photo['images']['low_resolution'] is not None:
				del self._photo['images']['low_resolution']
			if self._photo['images']['standard_resolution'] is not None:
				del self._photo['images']['standard_resolution']