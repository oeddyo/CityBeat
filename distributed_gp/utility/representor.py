from event_interface import EventInterface
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import linear_kernel

import re
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
        
        if vectorizer is None:
            self.vectorizer = TfidfVectorizer( max_df=0.7, min_df = 1, strip_accents='ascii', smooth_idf=True, preprocessor = self._preProcessor, sublinear_tf=True, norm = 'l2', analyzer='char_wb', ngram_range=(4,4))
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
        #print 'this type is ',type(cosine_similarities)
        #print centroid.shape, event_tfidf.shape
        cosine_similarities = np.asarray(self._cosine_sim(centroid, event_tfidf)).flatten()
        #print 'cosine type is ',type(cosine_similarities)

        most_related_pics = cosine_similarities.argsort()
        #print most_related_pics
        photos_to_return = []
        #print type(cosine_similarities)
        print event['_id']
        for idx in most_related_pics:
            print cosine_similarities[idx], event['photos'][idx]['link']
            photos_to_return.append( event['photos'][idx] )

        photos_to_return.reverse() 

        return photos_to_return 

    def getTfidfVector(self, event):
#        print 'the idx is ',self.vectorizer.get_feature_names()
#        print self.vectorizer.transform(self._getEventCaptions(event)).mean(axis=0)
        voc = self.vectorizer.get_feature_names()
        tf_vec = self.vectorizer.transform(self._getEventCaptions(event)).mean(axis=0)

#        print 'lens are ',len(voc),   tf_vec[0].shape

#        print 'words none-zero'
#        print self._getEventCaptions(event)

        nonzeros = np.nonzero(tf_vec)[1]
        res_list = nonzeros.ravel().tolist()[0] 

        values = []
        words = []
        for n in res_list:
            words.append( voc[n] )
            values.append( tf_vec[0,n] )

#        print words
#        print values
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


 
    #for event in rep.events:
        #print len(rep.getRepresentivePhotos( event ))
    #    print rep.getTfidfVector(event),'\n'
    
    
    for id in negative:
        for e in rep.events:
            if id == str(e['_id']):
                for p in rep.getRepresentivePhotos(e)[:10]:
                    print p['link']
                #print rep.getTfidfVector(e)
                print '\n'

if __name__ == '__main__':
    main()
