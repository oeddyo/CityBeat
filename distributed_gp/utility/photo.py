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
		
	def getCaption(self):
		if self._photo['caption'] is None:
			return ''
		if self._photo['caption']['text'] is None:
			return ''
		return self._photo['caption']['text']
	
	def toJSON(self):
		return self._photo
	
	def equalWith(self, photo):
		if not type(photo) is types.DictType:
			photo = photo.toJSON()
		if self._photo['id'] == photo['id']:
			return True
		return False