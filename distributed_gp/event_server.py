#!/usr/bin/python
# -*- coding: utf8 -*-

import cherrypy
import foursquare
#import config
import json
import time


from utility.event_interface import EventInterface
from utility.event_frontend import EventFrontend 
from utility.event import Event

from utility.event_feature import EventFeature
from utility.corpus import Corpus

class Root:
    def __init__(self):
        self.ei = EventInterface()
        #self.ei.setDB('AmazonMT')
        #self.ei.setCollection('candidate_event_25by25_merged')

        self.ei.setDB('citybeat')
        #self.ei.setCollection('next_week_candidate_event_25by25_merged')
        self.ei.setCollection('candidate_event_25by25')

        #collection = 'candidate_event_25by25_merged'
        #self.c = Corpus()
        #self.c.buildCorpusOnDB('AmazonMT', collection)
        
        collection = 'candidate_event_25by25'
        self.c = Corpus()
        self.c.buildCorpusOnDB('citybeat', collection)
        
        self._loadCrowdFlowerCode()

        self.cache_events = {}
        self.cache_photos = {}
        #self._cacheAll()

    def getAllEvents(self):
        event_cursor = self.ei.getAllDocuments()
        events = []
        limit = 10
        for e in event_cursor:
            if limit==0:
                break
            limit -= 1;
            #if e['label'] =='unlabeled':
            #    continue
            e['_id'] = str(e['_id'])
            e['urgency'] = 58
            e['volume'] = 99
            #e['photos'] = e['photos'][:min(5, len(e['photos']))] 
            e['stats'] = {'photos':50, 'tweets':0, 'checkins':0}

            events.append( e )
        return json.dumps(events)
    getAllEvents.exposed = True 
    
    def _loadCrowdFlowerCode(self):
        lines = open('crowdflower_code.txt').readlines()
        self.cf_code = {}
        for line in lines:
            t = line.split(',')
            self.cf_code[t[0]] = t[1]

    def getCrowdFlowerCode(self, event_id):
        if event_id in self.cf_code:
            return self.cf_code[event_id]
        else:
            return None
    getCrowdFlowerCode.exposed = True

    def getAllEventsIDs(self):
        object_ids = self.ei.getAllDocumentIDs()
        return_value = []
        for _id in object_ids:
            return_value.append( str(_id) )
        return json.dumps( return_value )
    #getAllEventsIDs.exposed = True
    
    def _deleteExtraMeta(self,photo):
        try: del photo['comments']
        except Exception as e: pass

        try: del photo['caption']['from']
        except Exception as e: pass
        try: del photo['filter']
        except Exception as e: pass
        try: del photo['user']
        except Exception as e: pass
        try: del photo['images']['standard_resolution']
        except Exception as e: pass
        try: del photo['images']['low_resolution']
        except Exception as e: pass
        try: del photo['likes']
        except Exception as e: pass
        try: del photo['likes']
        except Exception as e: pass
        return photo

    def getPhotosByID(self, event_id):
        if event_id in self.cache_photos:
            print 'cached. return directly'
            tmp = json.loads(self.cache_photos[event_id])
            to_return = []
            for idx in range(len(tmp)):
                tmp[idx][2] = [self._deleteExtraMeta(p) for p in tmp[idx][2] ]
            
            return json.dumps(tmp)
            #return self.cache_photos[event_id]
            #return self.cache_photos[event_id]
        event = self.ei.getEventByID(event_id)
        event = EventFrontend(event, self.c)
            
        #words_pics_list = event.getTopKeywordsAndPhotos(10, 6)
        top_words_list = event.getTopKeywordsAndPhotos(20,5)
        words_pics_list = event.getTopKeywordsAndPhotosByTFIDF(20, 5)
        keywords_shown = set()
        
        res = []
        for tf, idf in zip(top_words_list,words_pics_list):
            if tf[0] not in keywords_shown:
                keywords_shown.add(tf[0])
                res.append(tf)
            if idf[0] not in keywords_shown:
                keywords_shown.add(idf[0])
                res.append(idf)
        
        r = json.dumps(res) 
        #r = json.dumps(words_pics_list + top_words_list)
        return r
    getPhotosByID.exposed = True
   
    def _cacheAll(self):
        print 'begin cache'
        all_events = self.getAllEvents()
        print type(all_events)
        all_events = json.loads(all_events)
        cnt = 0
        for e in all_events:
            cnt+=1
            if cnt%100 == 0:
                print cnt
            self.cache_events[e['_id']] = json.dumps(e)
        for e in all_events:
            cnt+=1
            if cnt%100 == 0:
                print cnt
            self.cache_photos[e['_id']] = self.getPhotosByID(e['_id'])
          

    def getEventByID(self, event_id):
        if event_id in self.cache_events:
            tmp = json.loads(self.cache_events[event_id])
            tmp['photos'] = [ self._deleteExtraMeta(p) for p in tmp['photos']]

            return json.dumps( tmp )
            print 'event cached. return directly'
            #return self.cache_events[event_id]

        event = self.ei.getEventByID(event_id)
        event['_id'] = str(event['_id'])
        return json.dumps(event)
    getEventByID.exposed = True
    
    def getTopKeywords(self, event_id):
        event = self.ei.getEventByID(event_id)
        ef = EventFeature(event)
        words = ef.getTopKeywords(k=10)
        return json.dumps(words)
    #getTopKeywords.exposed = True

    def setLabel(self, event_id, label):
        event = self.ei.getEventByID(str(event_id))
        print 'setting ',event_id, 'label = ',label
        #event['label'] = int(label)
        event['label'] = int(label)
        self.ei.updateDocument( event ) 
    #setLabel.exposed = True

global_conf = {
        'global':{'server.environment': 'production',
            'engine.autoreload_on': True,
            'engine.autoreload_frequency':5,
            'server.socket_host': '0.0.0.0',
            'server.socket_port':7887,
            }
        }

cherrypy.config.update(global_conf)
cherrypy.quickstart(Root(), '/', global_conf)
