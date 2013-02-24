from utility.event_interface import EventInterface
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
from numpy import dot
from scipy.sparse import *
from sklearn.metrics.pairwise import linear_kernel

import re

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
            self.vectorizer = TfidfVectorizer( max_df=0.5, min_df = 2, strip_accents='ascii', smooth_idf=True, stop_words='english', preprocessor = self._preProcessor)
        else:
            self.vectorizer = vectorizer
        self.vectorizer.fit_transform(self._captions)
        print 'fitting tf-idf completed!'
    
    def _preProcessor(self, caption):
        regex = re.compile(r"#\w+")
        match = regex.findall(caption)
        if len(match)>=3:
            return ""
        else:
            return caption

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
            try:
                print event['photos'][idx]['location']['name']
            except:
                continue
        return 

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
