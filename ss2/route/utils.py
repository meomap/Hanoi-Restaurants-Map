'''
Created on Jun 4, 2012

@author: Hai1c09
'''
from django.db import connection
from django.contrib.gis.geos import LineString
import math
from route.models import Edge, Vertex

def distance(point1, point2):    
    """ Return the spherical distance between two point on the Earth surface. """
        
    lat1 = point1.x
    long1 = point1.y
    
    lat2 = point2.x
    long2 = point2.y
    
    rLat1 = math.radians(lat1)
    rLong1 = math.radians(long1)
    rLat2 = math.radians(lat2)
    rLong2 = math.radians(long2)
    
    dLat = rLat2 - rLat1
    dLong = rLong2 - rLong1
    a = math.sin(dLat/2)**2 + math.cos(rLat1) * math.cos(rLat2) \
                            * math.sin(dLong/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c
    
    return distance

def remove_vertex(vertex_id):
    """ Remove vertex & connected edges from graph. """
    
    v = Vertex.objects.get(id=vertex_id)
    Edge.objects.filter(vertex_end=v).delete()
    Edge.objects.filter(vertex_start=v).delete()
    v.delete()  
    
def match_vertex(location):
    """ Return the corresponding vertex for a given geometry. """
    
    cursor = connection.cursor()
    
    # Find the nearest edges for a given point
    sql = "SELECT id, ST_Distance(GeomFromText('POINT(%s %s)',4326),line) AS myLineDistance FROM route_edge ORDER BY myLineDistance LIMIT 3;" % (location.x, location.y)
    cursor.execute(sql)
    row = cursor.fetchone()
    edge_id = row[0]
    print "nearest road is ", Edge.objects.get(id=edge_id).name
    
    # Find the closest point on the previous edge
    sql = "SELECT AsText(ST_Line_Interpolate_Point(line,ST_Line_Locate_Point(line,GeomFromText('POINT(%s %s)', 4326)))) FROM route_edge WHERE id = %s;" % (location.x, location.y, row[0])
    cursor.execute(sql)
    row = cursor.fetchone()    
    closestpt = row[0]
    
    # Add this point to graph
    id = (Vertex.objects.latest('id').id) + 1
    print "id is ", id
    v = Vertex(id=id, pt=closestpt)
    v.save()
    
    # Make edges connect to this point
    e = Edge.objects.get(id=edge_id)
    e_start = e.vertex_start
    e_end = e.vertex_end
    
    cost1 = distance(e_start.pt, v.pt)
    e1 = Edge(name=e.name, cost=cost1, reverse=e.reverse, 
        line=LineString([e_start.pt, v.pt]), 
        vertex_start=e_start, vertex_end=v)
    e1.save()
    
    cost2 = distance(v.pt, e_end.pt)
    e2 = Edge(name=e.name, cost=cost2, reverse=e.reverse, 
        line=LineString([v.pt, e_end.pt]), 
        vertex_start=v, vertex_end=e_end)
    e2.save()
    
    return v

def select_vertexs(startpt, endpt):
    """ Return the relevant start & end vertex on graph """ 
    
    start_vertex = match_vertex(startpt) 
    end_vertex = match_vertex(endpt)
    
    return (start_vertex, end_vertex)  