#!/usr/bin/python
# -*- coding: utf8 -*-

import cherrypy
import foursquare
#import config
import json
import time


from utility.event_interface import EventInterface
from utility.event import Event

from utility.event_feature import EventFeature


class Root:
    def __init__(self):
        self.ei = EventInterface()
        self.ei.setCollection('candidate_event_10by10_merged')
        pass
    def getAllEvents(self):
        event_cursor = self.ei.getAllDocuments()
        events = []
        limit = 300
        for e in event_cursor:
            limit -=1
            if e['label'] == 'unlabeled':
                e['label'] = 0
            e['_id'] = str(e['_id'])
            events.append( e )
            if limit==0:
                break
        return json.dumps(events)
    getAllEvents.exposed = True 
    
    def getEventByID(self, event_id):
        event = self.ei.getEventByID(event_id)
        event['_id'] = str(event['_id'])
        return json.dumps(event)
    getEventByID.exposed = True
    
    def getTopKeywords(self, event_id):
        event = self.ei.getEventByID(event_id)
        ef = EventFeature(event)
        words = ef.getTopKeywords(k=10)
        return json.dumps(words)
    getTopKeywords.exposed = True

    def setLabel(self, event_id, label):
        #label = str(label)
        #event = self.ei.getEventByID(event_id)
        #event.setLabel(int(label))
        #self.ei.updateDocument(event)
        print 'setting ',event_id, 'label = ',label
    setLabel.exposed = True

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
