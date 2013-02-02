from photo_interface import PhotoInterface



if __name__=="__main__":
	pi = PhotoInterface()
	pi.setCollection('photos')
	
	pi2 = PhotoInterface()
	pi2.setCollection('photos_no_duplicate')
	
	photos = pi.getAllDocuments()
	id_set = set()
	for photo in photos:
		if not photo['id'] in id_set:
			id_set.add(photo['id'])
			photo['_id'] = photo['id']
			pi2.saveDocument(photo)