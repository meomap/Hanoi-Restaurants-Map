'''
Created on Jun 2, 2012   
    Run this script to populate edge & vertex tables with data from
    OSM XML file
@author: meo map
'''
from route.models import Vertex, Edge
from django.contrib.gis.geos import Point, LineString
from xml import sax
from utils import distance

#__________________________________________________________________
# Vertex parsing

class VertexHandler(sax.handler.ContentHandler):

    def __init__(self):
        sax.handler.ContentHandler.__init__(self)
        self.id = None
        self.geometry = None
        self.vertexs = {}

    def startElement(self, name, attrs):
        if name == 'node':            
            self.id = int(attrs['id'])
            self.tags = {}
            self.geometry = map(
                float, (attrs['lon'], attrs['lat']))
        elif name == 'tag' and self.id:            
            self.tags[attrs['k']] = attrs['v']

    def endElement(self, name):
        if name == 'node':
            n = Vertex(id=self.id, pt=Point(self.geometry[0], self.geometry[1]))            
            n.save()
            self.vertexs[self.id] = n
            
            self.id = None
            self.geometry = None
            self.tags = None



#__________________________________________________________________
# Way parsing

class WayHandler(sax.handler.ContentHandler):

    def __init__(self, vertexs):
        self.id = None;
        self.geometry = None;
        self.ways = {}
        self.vertexs = vertexs      # All reference Vertexs

    def startElement(self, name, attrs):
        if name == 'way':
            self.id = int(attrs['id'])
            self.tags = {}
            self.geometry = []

        elif name == 'nd':
            self.geometry.append(int(attrs['ref']))

        elif name == 'tag' and self.id:
            self.tags[attrs['k']] = attrs['v']

    def reset(self):
        self.id = None
        self.geometry = None
        self.tags = None


    def makeEdges(self):
        name = ""
        if "name" in self.tags:
            name = self.tags["name"]
        
        for i in range(len(self.geometry)-1):
            # retrieve related Vertexs        
            startVertex = self.vertexs[self.geometry[i]] 
            endVertex = self.vertexs[self.geometry[i+1]]
            
            # additional attributes
            reverse = True
            if 'oneway' in self.tags:
                if self.tags['oneway'] == "yes" or self.tags['oneway'] == "1":
                    reverse = False
            cost = distance(startVertex.pt, endVertex.pt)
            
            # make edge
            edge = Edge(name=name, cost=cost, reverse=reverse, 
                        line=LineString([startVertex.pt, endVertex.pt]), 
                        vertex_start=startVertex, vertex_end=endVertex)
            edge.save()
  

    def endElement(self, name):
        if name == 'way':
            
            # process way only
            if 'highway' in self.tags:
                if len(self.geometry) > 1:                                       
                    self.makeEdges()
            self.reset()



def extract(osm):
    print "Extracting road in " + osm;
    
    print "Parsing Vertex ..."
    vertexhandler = VertexHandler()
    
    parser = sax.make_parser()
    parser.setContentHandler(vertexhandler)
    parser.parse("data/"+osm)
    print "Loaded ", Vertex.objects.count(), " Vertexs"
    
    vertexs = vertexhandler.vertexs       # dict of Vertexs. keyed by their ids
    
    print "Ok. Now Parsing Way ..."
    wayhandler = WayHandler(vertexs)
    parser.setContentHandler(wayhandler)
    
    parser.parse("data/"+osm)
    print "Loaded ", Vertex.objects.count(), " Edges"
    
    # Remove unnecessary vertexs
    print "Refine data"
    vertexs = Vertex.objects.all()
    count = 0;
    for v in vertexs:
        lst1 = Edge.objects.filter(vertex_start=v)
        lst2 = Edge.objects.filter(vertex_end=v)
        if len(lst1) == 0 or len(lst2) == 0:
            v.delete()
            count += 1
            
    print "Remove %s vertexs" % count
    
    
if __name__ == '__main__':
    extract("map_large.osm")