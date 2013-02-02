class Photo:
	def __init__(self, photo):
		self._photo = photo
	
	def getLocations(self):
		lat = float(self._photo['location']['latitude'])
		lon = float(self._photo['location']['longitude'])
		return lat, lon
		
	def getCaption(self):
		if self._photo['caption'] is None:
			return ''
		if self._photo['caption']['text'] is None:
			return ''
		return self._photo['caption']['text']