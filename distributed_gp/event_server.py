#!/usr/bin/python
# -*- coding: utf8 -*-

import cherrypy
import foursquare
import config
import json
import time


from utility.event_interface import EventInterface
from utility.event import Event



class Root:
    def __init__(self):
        self.ei = EventInterface('candidate_event_10by10')
        pass
    
    def getAllEvents(self):
        events = ei.getAllDocuments()
        print events[0]


    get_foursquare_heatmap.exposed = True

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
