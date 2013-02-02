from photo_interface import PhotoInterface



if __name__=="__main__":
	pi = PhotoInterface()
	pi.setCollection('photos')
	pi2 = PhotoInterface()
	
	photos = pi.getAllDocuments()
	id_set = set()
	link_set = set()
	for photo in photos:
		id_set.add(photo['id'])
		link_set.add(photo['link'])
	print len(id_set)
	print len(link_set)
		