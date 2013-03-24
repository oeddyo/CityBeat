from event_interface import EventInterface
from event import Event
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import linear_kernel
from tweet_cluster import TweetCluster

import re
class Representor():
    def __init__(self, vectorizer = None, twitter = False):
        """Given an event, return a list incices of the photos in 'photos' filed 
        which are representative to stands for this cluster
        
        Could overwrite TfidfVectorizer as a parameter so that you could customize
        your own tfidf parameters. 
        see http://scikit-learn.org/dev/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        """
        
        self.ei = EventInterface()
        self.ei.setDB('AmazonMT')
        self.ei.setCollection('candidate_event_25by25_merged')
        self.events = []
        for e in self.ei.getAllDocuments():
            event = Event(e)
            event.selectOnePhotoForOneUser()
            e = event.toJSON()
            self.events.append(e)
        #self.events = [e for e in self.ei.getAllDocuments()]
        self._captions = self._getAllCaptions()
        
        if vectorizer is None:
            self.vectorizer = TfidfVectorizer( max_df=0.05, min_df = 1, strip_accents='ascii', smooth_idf=True, preprocessor = self._preProcessor, sublinear_tf=True, norm = 'l2', analyzer='char_wb', ngram_range=(4,4), stop_words = 'english')
        else:
            self.vectorizer = vectorizer
        self.vectorizer.fit_transform(self._captions)
#        print self.vectorizer.get_feature_names()
    def _preProcessor(self, caption):
        regex = re.compile(r"#\w+")
        match = regex.findall(caption)
        if len(match)>=5:
            return ""
        else:
            return caption

    def _getAllCaptions(self):
        _captions = []
        for event in self.events:
            _captions += self._getEventCaptions(event)
        return _captions

    def _is_ascii(self, _str):
        return all(ord(c) < 128 for c in _str)

    def _getEventCaptions(self, event):
        """For a given event, return the captions as a list. Note for photo without caption,
        use a None to hold the place"""
        event_captions = []
        for p in event['photos']:
            try:
                if self._is_ascii(p['caption']['text']):
                    event_captions.append( p['caption']['text'].lower() )
                else:
                    event_captions.append("")
            except:
                event_captions.append( "" )
        return event_captions 
    def _cosine_sim(self, a, b):
        return a*b.T
    
    def getRepresentivePhotos(self, event):
        
        event_captions = self._getEventCaptions(event)
        event_tfidf = self.vectorizer.transform(event_captions)
        
        centroid = event_tfidf.mean(axis=0)
        #cosine_similarities = linear_kernel(centroid, event_tfidf).flatten()
        cosine_similarities = np.asarray(self._cosine_sim(centroid, event_tfidf)).flatten()

        most_related_pics = cosine_similarities.argsort()
        photos_to_return = []
        #print event['_id']
        for idx in most_related_pics:
#            print cosine_similarities[idx], event['photos'][idx]['link']
            photos_to_return.append( event['photos'][idx] )
        photos_to_return.reverse() 

        return photos_to_return 

    def getTfidfVector(self, event):
        voc = self.vectorizer.get_feature_names()
        tf_vec = self.vectorizer.transform(self._getEventCaptions(event)).mean(axis=0)

        nonzeros = np.nonzero(tf_vec)[1]
        res_list = nonzeros.ravel().tolist()[0] 

        values = []
        words = []
        for n in res_list:
            words.append( voc[n] )
            values.append( tf_vec[0,n] )

        return res_list, words, values

    def getCorpusWordsVector(self):
        return self.vectorizer.get_feature_names()


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
    #print rep.getCorpusWordsVector()


 
    
    for id in positive:
        for e in rep.events:
            if id == str(e['_id']):
                for p in rep.getRepresentivePhotos(e)[:10]:
                    pass
                    #print p['link']
                #print rep.getTfidfVector(e)
#                print '\n'

if __name__ == '__main__':
    main()
