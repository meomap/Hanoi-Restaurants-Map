from route.utils import remove_vertex, select_vertexs
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from route.models import Vertex
from django.http import HttpResponse
from core.search import uniformCostSearch
from core.searchAgents import GraphProblem
from core.utils import *


import json


def search_route(request):
    # Extract initial & goal location
    locations = map (float, request.GET['locations'].split(","))
        
    startpt = Point(locations[0], locations[1])
    endpt = Point(locations[2], locations[3]) 

    # Look up for initial & end vertex
    startVertex, endVertex = select_vertexs(startpt, endpt)

    # Get initial vertex & goal vertex id
    startId = startVertex.id
    endId = endVertex.id
    
    print "routing for", startId, endId
    
    # Find the route
    routes = route_vertexs(startId, endId)    
    routes[:0] = [[endpt.x, endpt.y]]
    routes.append([startpt.x, startpt.y])
     
    # Convert to GeoJSON
    geojson_dict = {
            "type": "FeatureCollection",
            "features": [{            
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": routes
                },
                "properties": {
                    "id": "id"
            }
        }]
    }
    
    # Return the response
    return HttpResponse(json.dumps(geojson_dict), 
                        content_type="application/json")

                            
def route_vertexs(startId, endId):
    """ Return a routes between the given vertex ids """
    
    # invoke search algorithm
    ab = GraphProblem(startId, endId)
    goal = uniformCostSearch(ab)
    solution = [node.state for node in goal.path()] # node state is vertex id
    routes = []
    print str(solution)
    # create route
    for vertex_id in solution:
        vertex_pt = Vertex.objects.get(id=vertex_id).pt
        routes.append([vertex_pt.x, vertex_pt.y])
           
    routes = routes[:]
    # remove start & end vertex
    remove_vertex(startId)
    remove_vertex(endId)
    
    return routes
