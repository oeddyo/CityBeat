from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface
from kl_divergence import kldiv
from kl_divergence import tokenize
import networkx as nx
import math
import community
import time
from time import mktime
from datetime import datetime



class EventGraph():
    def __init__(self):
        self.events = None
        
    def readEvent(self):
        mongoDB = MongoDBInterface('grande',27017)
        #mongoDB.SetDB('alarm_filter')
        #mongoDB.SetCollection('photos')
        mongoDB.SetDB('historic_alarm')
        mongoDB.SetCollection('raw_event')
        self.events = mongoDB.GetAllItems()
    
    def _locationDistance(self,location_a, location_b):  #compute distance of two lat/lng pairs 
        return math.sqrt((location_a[0]-location_b[0])*(location_a[0]-location_b[0]) + (location_a[1]-location_b[1])*(location_a[1]-location_b[1]))

    def _getLocationPair(self, photo_json):
        return (photo_json['location']['latitude'], photo_json['location']['longitude'])
    
    def _getTime(self, photo_json):
        return int(photo_json['created_time'])

    def _getCaption(self, photo_json):
        return photo_json['caption']['text']

    def doEventModularity(self, event):
        node_mapping = {}
        node_cnt = 0
        G = nx.Graph()  #graph 
        photos = event['photos']
        for p in photos:
            node_mapping[node_cnt] = p
            G.add_node(node_cnt)
            node_cnt+=1
        
        dis_max = 1e-10
        for node_a in G.nodes():
            for node_b in G.nodes():
                if node_a<node_b:
                    G.add_edge(node_a,node_b, weight=0.0)
                    dis_max = max( dis_max, self._locationDistance( self._getLocationPair(node_mapping[node_a]), self._getLocationPair(node_mapping[node_b])))
        
        for node_a in G.nodes():
            for node_b in G.nodes():
                if node_a < node_b:
                    G[node_a][node_b]['weight'] =  1.0*(1 - self._locationDistance( self._getLocationPair(node_mapping[node_a]), self._getLocationPair(node_mapping[node_b]))*1.0/dis_max )
                    #assert G[node_a][node_b]['weight'] <= 1.0, 'error here'
                    continue
        time_interval_max = 1e-10
        for node_a in G.nodes():
            for node_b in G.nodes():
                if node_a < node_b:
                    time_interval_max = max(time_interval_max, abs(self._getTime(node_mapping[node_a]) - self._getTime(node_mapping[node_b])) )
        print 'time_max = ',time_interval_max
        for node_a in G.nodes():
            for node_b in G.nodes():
                if node_a < node_b:
                    time_interval = 1 - abs(self._getTime(node_mapping[node_a]) - self._getTime(node_mapping[node_b]))*1.0/(time_interval_max+1)
                    G[node_a][node_b]['weight'] +=  0.1*time_interval
        kl_max = 1e-10

        for node_a in G.nodes():
            for node_b in G.nodes():
                if node_a < node_b:
                    # Symmetric KL 
                    try:
                        caption_a = tokenize(self._getCaption(node_mapping[node_a]))
                        caption_b = tokenize(self._getCaption(node_mapping[node_b]))
                        kl_max = max(kl_max, kldiv(caption_a, caption_b) + kldiv(caption_b, caption_a) )
                    except:
                        #Caption might doesn't exist
                        #Exception might be thrown in KL
                        continue
         
        for node_a in G.nodes():
            for node_b in G.nodes():
                if node_a < node_b:
                    # Symmetric KL 
                    try:
                        caption_a = tokenize(self._getCaption(node_mapping[node_a]))
                        caption_b = tokenize(self._getCaption(node_mapping[node_b]))
                        kl_value = 1- (kldiv(caption_a, caption_b) + kldiv(caption_b, caption_a)) *1.0 / kl_max
                        G[node_a][node_b]['weight'] += 0.5*kl_value
                        
                        if G[node_a][node_b]['weight'] < 0.6:
                            G.remove_edge(node_a, node_b)
                    except:
                        #Caption might doesn't exist
                        #Exception might be thrown in KL
                        continue
        for node_a in G.nodes():
            for node_b in G.nodes():
                try:
                    #print node_a, node_b, G[node_a][node_b]
                    continue
                except:
                    continue
        print '\n\n'

        partition = community.best_partition(G)

        #print partition
        print '--------------event----------------- ' 
        cluster = {}
        for key in partition:
            if partition[key] in cluster:
                cluster[partition[key]].append(key)
            else:
                cluster[partition[key]] = [ key]
        
        for c in cluster.values():
            for p in c:
                dt = time.gmtime(int(node_mapping[p]['created_time']))
                dt = datetime.fromtimestamp(mktime(dt))

                print node_mapping[p]['link'], dt

            tmp_sum = 0.0
            tmp_cnt = 0
            for node_a in c:
                for node_b in c:
                    if node_a<node_b and G.has_edge(node_a,node_b):
                        tmp_sum += G[node_a][node_b]['weight']
                        tmp_cnt +=1
            print 'avg weight ',tmp_sum*1.0/tmp_cnt

                        
            print '\n'

def main():
    eg = EventGraph()
    eg.readEvent()
    cnt = 0
    for e in eg.events:
        if len(e['photos'])>15:
            cnt+=1
            eg.doEventModularity(e)
main()
