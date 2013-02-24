from utility.event_interface import EventInterface
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
from numpy import dot
from scipy.sparse import *
from sklearn.metrics.pairwise import linear_kernel

#from sklearn.metrics.pairwise import euclidean_distances


class Representor():
    def __init__(self, vectorizer = None):
        """Given an event, return a list incices of the photos in 'photos' filed 
        which are representative to stands for this cluster
        
        Could overwrite TfidfVectorizer as a parameter so that you could customize
        your own tfidf parameters. 
        see http://scikit-learn.org/dev/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        """

        self.ei = EventInterface()
        self.ei.setDB('citybeat')
        self.ei.setCollection('candidate_event_25by25_merged')

        self.events = [e for e in self.ei.getAllDocuments()]
        self._captions = self._getAllCaptions()
        
        print '# of all captions ',len(self._captions)
        print 'begin fitting tf-idf...'

        if vectorizer is None:
            self.vectorizer = TfidfVectorizer( max_df=0.5, min_df = 2, strip_accents='ascii', smooth_idf=True, stop_words='english')
        else:
            self.vectorizer = vectorizer
        self.vectorizer.fit_transform(self._captions)
        print 'fitting tf-idf completed!'

    def _getAllCaptions(self):
        _captions = []
        for e in self.events:
            caption = ""
            for p in e['photos']:
                try:
                    text = p['caption']['text']
                    if text is not None:
                        _captions.append(text) 
                except:
                    print 'error'
                    continue
        return _captions

    def _cosine(self,y, centroid):
        above = y*centroid.T
        above = above[0,0]
        below = (y*y.T) 
        below = sqrt(below[0,0])
        below2 = centroid*centroid.T
        below2 = sqrt( below2[0,0] )
        if below==0 or below2 == 0:
            return 0.0
        return above*1.0/(below*below2)
    def _getEventCaptions(self, event):
        """For a given event, return the captions as a list. Note for photo without caption,
        use a None to hold the place"""
        event_captions = []
        for p in event['photos']:
            try:
                event_captions.append( p['caption']['text'] )
            except:
                event_captions.append( "" )
        return event_captions 
    
    def getRepresentivePhotos(self, event):
        #event = self.ei.getEventByID(event_id)

        # now for each event
        # get the photos, and get the tf-idf score. get centroid
        # and compute the cloestest top 5
        #for event in self.events:
          
        print event['_id']
        
        event_captions = self._getEventCaptions(event)
        print 'before trans'
        print event_captions
        event_tfidf = self.vectorizer.transform(event_captions)
        print 'end trans'
        centroid = event_tfidf.mean(axis=0)
        cosine_similarities = linear_kernel(centroid, event_tfidf).flatten()
        most_related_pics = cosine_similarities.argsort()[:-10:-1]
        for idx in most_related_pics:
            print event['photos'][idx]['link']
        return 


        res = [ ] 
        print 'large trans'
        for doc,link,loc,time in zip(docs, links, locs, times):
            y = self.vectorizer.transform([doc,])
            res.append( (self._cosine(y, centroid), link, loc, time) ) 
        print 'end large trans'
        sorted_res = sorted(res, key=lambda tup: tup[0] )
        print 'length is ',len(sorted_res)
        sorted_res.reverse()
        #if sorted_res[0][0]<0.4:
        #    return 
        print '---- top tf-idf -----' 
        print sorted_res[:10]
        if sorted_res[0][2] == sorted_res[1][2]:
            #and sorted_res[1][2] == sorted_res[2][2] :
            #and sorted_res[2][2] == sorted_res[3][2]:
            self.full_fill_count += 1
        

        places_dic = {}
        for place in sorted_res[:10]:
            if place[2] not in places_dic:
                places_dic[place[2]] = 1
            else:
                places_dic[place[2]] += 1

        #print '-----top degrees ----'
        
        common_place_cnt = max( places_dic.values())
        ratio = common_place_cnt*1.0/len(sorted_res)
        
        self.ratio_count_all+=1
        if ratio>=0.2:
            self.ratio_count+=1
        print 'new ratio ', self.ratio_count*1.0/self.ratio_count_all
            
        """
            for a in docs:
                for b in docs:
                    if a<b:
                        t_a = self.vectorizer.transform(a)
                        t_b = self.vectorizer.transform(b)
                        if self._cosine(t_a, t_b)>=0.05:
                            degrees[docs.index(t_a)]+=1
                            degrees[docs.index(t_b)]+=1
            sorted_index = [i[0] for i in sorted(enumerate(degrees), key=lambda x:x[1])]
            mylinks = [ links[idx] for idx in sorted_index[:5]]
            print mylinks

            print 'current ratio %d / %d = %f'%(self.full_fill_count, self.tmp_count, self.full_fill_count*1.0/self.tmp_count)
        """
        return  
        """
        print type(X_train)
        print dir(X_train)
        print type(X_train[0])
        print X_train[0]
        print 'all words',len(vectorizer.get_feature_names())
        print vectorizer.get_feature_names()
        """

def main():


    #read labels and ids
    lines = open('label_data_csv2.txt').readlines()
    positive = []
    negative = []
    for line in lines:
        t = line.split()
        if t[1]=='1':
            positive.append(t[0])
        elif t[1]=='-1':
            negative.append(t[0])
    rep = Representor()

    for event in rep.events:
        rep.getRepresentivePhotos( event )
    
    return 
    for id in positive:
        for e in rep.events:
            if id == str(e['_id']):
                rep.getRepresentivePhotos( e )
main()
