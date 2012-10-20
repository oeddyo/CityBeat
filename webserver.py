#!/usr/bin/python
# -*- coding: utf8 -*-

import cherrypy
import foursquare
import config
import json
import time
from lib.mysql_connect import connect_to_mysql
class Root:
    def __init__(self):
        pass
    def get_current_heatmap(self):
        sql = """select * from herenow_region order by time desc limit 2000"""
        cursor = connect_to_mysql()
        cursor.execute(sql)
        res = []
        tset = set()
        for r in cursor.fetchall():
            x = r['mid_lat']
            y = r['mid_lng']
            if (x,y) in tset:
                continue
            else:
                tset.add( (x,y))
            res.append( (r['mid_lat'], r['mid_lng'], r['herenow']) )
        print len(tset)
        return json.dumps(res)
    get_current_heatmap.exposed = True


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
