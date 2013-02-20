from utility.event_interface import EventInterface
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
from numpy import dot
from scipy.sparse import *
from sklearn.naive_bayes import MultinomialNB


#from sklearn.metrics.pairwise import euclidean_distances


class Representor():
    def __init__(self):
        self.ei = EventInterface()
        self.ei.setDB('citybeat')
        self.ei.setCollection('candidate_event_25by25_merged')
        self.events = [e for e in self.ei.getAllDocuments()]
        
        self._getAllCaptions()
        print 'all docs ',len(self.docs)

        self.vectorizer = TfidfVectorizer( max_df=0.5, min_df = 2, strip_accents='ascii', smooth_idf=True, stop_words='english')
        tfidf = self.vectorizer.fit_transform(self.docs)
        
        self.tmp_count = 0
        self.full_fill_count = 0

        print tfidf[0]
        return 
    def _filterText(self, text):
        return text

    def _getCaptionsWithLinks(self, event):
        caps = []
        links = []
        locs = []
        times = []
        user_dic = set()
        for p in event['photos']:
            try:
                cap = p['caption']['text']
                link = p['link']
                loc = p['location']['name']
                time = p['created_time']
                if p['user']['username'] in user_dic:
                    continue
                else:
                    user_dic.add(p['user']['username'])
                caps.append(cap)
                links.append(link)
                locs.append(loc)
                times.append( time)
            except:
                continue
        return caps,links,locs, times

    def _getAllCaptions(self):
        self.docs = []
        cnt = 0
        for e in self.events:
            #if cnt==10:break
            caption = ""
            for p in e['photos']:
                try:
                    text = self._filterText(p['caption']['text'])
                    self.docs.append( text )
                    self.mapping_dic[ text  ] = cnt 
                    cnt += 1
                except :
                    continue
    
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

    def getRepresentivePhotos(self, event_id):
        
        event = self.ei.getEventByID(event_id)

        # now for each event
        # get the photos, and get the tf-idf score. get centroid
        # and compute the cloestest top 5
        #for event in self.events:

        docs,links, locs, times = self._getCaptionsWithLinks(event)
        degrees = [0]*len(docs)
        
        if len(docs)<5:
            print 'negative directly jump'
            return 
        if len(docs)>5 :
            self.tmp_count+=1
            ys = self.vectorizer.transform(docs)
            centroid = ys.mean(axis=0)
            res = [ ] 
            for doc,link,loc,time in zip(docs, links, locs, times):
                y = self.vectorizer.transform([doc,])
                res.append( (self._cosine(y, centroid), link, loc, time) ) 

            sorted_res = sorted(res, key=lambda tup: tup[0] )
            sorted_res.reverse()
            if sorted_res[0][0]<0.4:
                return 
            print '---- top tf-idf -----' 
            print sorted_res[:10]
            if sorted_res[0][2] == sorted_res[1][2]:
                #and sorted_res[1][2] == sorted_res[2][2] :
                #and sorted_res[2][2] == sorted_res[3][2]:
                self.full_fill_count += 1

            print '-----top degrees ----'

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
    lines = open('labels.txt').readlines()
    positive = []
    negative = []
    for line in lines:
        t = line.split()
        if t[1]=='1':
            positive.append(t[0])
        elif t[1]=='-1':
            negative.append(t[0])
    rep = Representor()

    for id in positive:
        print id
        rep.getRepresentivePhotos( id )
main()
