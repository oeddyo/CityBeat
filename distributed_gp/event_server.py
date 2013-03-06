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

from utility.representor import Representor

from utility.event_feature import EventFeature
from utility.corpus import Corpus

import random




class Root:
    def __init__(self):
        self.ei = EventInterface()
        self.ei.setDB('AmazonMT')
        self.ei.setCollection('candidate_event_25by25_merged')
        self.representor = Representor()
        #self.ei.setDB('citybeat')
        #self.ei.setCollection('next_week_candidate_event_25by25_merged')
        #self.ei.setCollection('online_candidate')
        
        self._loadCrowdFlowerCode()


    def getAllEvents(self):
        event_cursor = self.ei.getAllDocuments()
        events = []
        tmp_events = [e for e in event_cursor]
        for e in tmp_events:
            if len(e['photos'])>3:
                if random.random()>0.1:
                    e['_id'] = str(e['_id'])
                    e['urgency'] = 58
                    e['volume'] = 99
                    e['stats'] = {'photos':50, 'tweets':0, 'checkins':0}
                    rep_photos = self.representor.getRepresentivePhotos(e)
                    e['photos'] = rep_photos[:min(5,len(rep_photos))]
                    events.append(e)
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
        event = json.loads(self.getEventByID(event_id))
        #event = EventFrontend(event, self.c)
            
        #top_words_list = event.getTopKeywordsAndPhotos(20,5)
        #words_pics_list = event.getTopKeywordsAndPhotosByTFIDF(20, 5)
        #keywords_shown = set()
        
        res = []

        all_photos = []
        top10_photos = []
        all_photos.append('all_photos')
        #print event['photos']
        all_photos.append(len(event['photos']))
        all_photos.append( event['photos'])

        rep_photos = self.representor.getRepresentivePhotos(event)
        rep_photos = rep_photos[:10]
        top10_photos.append('top_10_representative')
        top10_photos.append(min(10, len(rep_photos)))
        top10_photos.append(rep_photos)
   
        res.append(all_photos)
        res.append(top10_photos)
        """
        for tf, idf in zip(top_words_list,words_pics_list):
            if tf[0] not in keywords_shown:
                keywords_shown.add(tf[0])
                res.append(tf)
            if idf[0] not in keywords_shown:
                keywords_shown.add(idf[0])
                res.append(idf)
        """ 
        r = json.dumps(res) 
        #print r
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
        event = self.ei.getEventByID(event_id)
        event = Event(event)
        event.selectOnePhotoForOneUser()
        event_dic = event.toJSON()
        event_dic['_id'] = str(event_dic['_id'])
        return json.dumps(event_dic)
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
