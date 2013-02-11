class Stopwords:
	@staticmethod
	def stopwords():
		self_defined = set(['nyc', 'ny', 'new', 'york', 'newyork', 'park', 'central', 'day', 'christmas', 'xmas'])
		nltk_list = (['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
											 'ourselves', 'you', 'your', 'yours', 'yourself',
								 			 'yourselves', 'he', 'him', 'his', 'himself', 
								 'she', 'her', 'hers', 'herself', 'it', 'its', 
								 'itself', 'they', 'them', 'their', 'theirs', 
								 'themselves', 'what', 'which', 'who', 'whom', 
								 'this', 'that', 'these', 'those', 'am','is', 
								 'are', 'was', 'were', 'be', 'been', 'being', 
								 'have', 'has', 'had', 'having', 'do', 'does', 
								 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 
								 'if', 'or', 'because', 'as', 'until', 'while', 
								 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
								 'between', 'into', 'through', 'during', 'before', 
								 'after', 'above', 'below', 'to', 'from', 'up', 
								 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
								 'further', 'then', 'once', 'here', 'there', 'when', 
								 'where', 'why', 'how', 'all', 'any', 'both', 'each', 
								 'few', 'more', 'most', 'other', 'some', 'such', 'no',
								 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 
								 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
								 'should', 'now'])
		topwords = (['love', 'happy', 'night', 'time', 'city', 'like', 'manhattan', 'm', 'good', 'thanksgiving', 'tree', 'one', 'instagood', 'best', 'beautiful', 'lol', 'newyorkcity', 'square', 'birthday', 'today', 'holiday', 'work', 'party', 'get', 'life', 'art', 'fun', 'fashion', 'food', 'times', 'tbt', 'friends', 'last', 'morning', 'got', 'dinner', 'go', 'lights', 'brooklyn', 'photooftheday', 'picoftheday', 'back', 'instamood', 'amazing', 'girl', 'cute', 'year', 'building', 'see', 'look', 'home', 'little', 'first', 'igers', 'view', 'thanks', 'holidays', 'instadaily', 'nofilter', 'empire', 'w', 'family', 'follow', 'ever', 'pretty', 'tonight', 'state', 'th', 'big', 'iphonesia', 'winter', 'rockefeller', 'baby', 'oh', 'made', 'know', 'world', 'instagram', 'show', 'great', 'right', 'photo', 'favorite', 'timessquare', 'street', 'd', 'igdaily', 'awesome', 'much', 'bestoftheday', 'us', 'style', 'black', 'music', 'people', 'iphoneonly', 're', 'com', 'getting', 'red', 'center', 'lunch', 'way', 'ready', 'instagramhub', 'hot', 'cool', 'cold', 'shopping', 'going', 'come', 'santa', 'de', 'man', 'friday', 'sky', 'u', 'want', 'foodporn', 'still', 'never', 'girls', 'miss', 'old', 'parade', 'webstagram', 'really', 'always', 'yum', 'subway', 'broadway', 'place', 'thank', 'rock', 'chocolate', 've', 'centralpark', 'bar', 'make', 'friend', 'merry', 'live', 'soho', 'yes', 'take', 'office', 'jj', 'usa', 'years', 'hair', 'st', 'nice', 'top', 'sunday', 'think', 'ice', 'finally', 'real', 'store', 'picstitch', 'two', 'better', 'la', 'let', 'brunch', 'need', 'macy', 'pic', 'blue', 'picture', 'o', 'n', 'macys', 'found', 'knicks', 'coffee', 'looking', 'face', 'hello', 'shit', 'iphone', 'waiting', 'boy', 'crazy', 'y', 'another', 'sweet', 'next', 'white', 'light', 'mom', 'guys', 'breakfast', 'grand', 'yummy', 'dog', 'empirestatebuilding', 'well', 'funny', 'free', 'likes', 'guy', 'long', 'perfect', 'everyone', 'room', 'summer', 'house', 'delicious', 'days', 'train', 'even', 'things', 'wait', 'apple', 'msg', 'game', 'x', 'nye', 'season', 'school', 'll', 'would', 'drinks', 'done', 'thing', 'sun', 'fall', 'say', 'swag', 'believe', 'gift', 'timesquare', 'looks', 'stop', 'window', 'e', 'bday', 'check', 'concert', 'christmastree', 'hotel', 'instagramers', 'beer', 'beauty', 'lmao', 'snow', 'please', 'week', 'sunset', 'wine', 'tweegram', 'followme', 'every', 'post', 'feel', 'around', 'pizza', 'santacon', 'making', 'december', 'ladies', 'early', 'shop', 'true', 'bad', 'sexy', 'haha', 'hey', 'architecture', 'latergram', 'instahub', 'en', 'photography', 'hard', 'many', 'ig', 'saturday', 'ave', 'sister', 'cake', 'late', 'green', 'coming', 'weekend', 'shots', 'skating', 'turkey', 'dessert', 'america', 'shoes', 'b', 'pink', 'team', 'smile', 'chicken', 'taking', 'working', 'da', 'cheese'])
		return self_defined.union(nltk_list).union(topwords)