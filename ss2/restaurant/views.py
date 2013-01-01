# Create your views here.
from django.template import Context, loader
from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis.measure import D
from route.utils import distance
from restaurant.models import Restaurant, Category
from django.http import HttpResponse
import json


"""
    Loading page first time
"""
def index(request):
    t = loader.get_template('restaurant.html')
    # Retrieve all categories in hierarchy order
    main_categories = Category.objects.filter(super_cat='')
    categories = [{"cat": item, 
                   "sub_cats": Category.objects.filter(super_cat=item.name)
                   } 
                  for item in main_categories]
    c = Context({
            'categories': categories
    })
    return HttpResponse(t.render(c))


"""
    Return a list of restaurants based on current bounding box
"""
def restaurant_list(request):
    # /restaurant.json?bbox=21.098,30.999,10.043,-24.00&cat=1,2,3    
    # Figure out the bounding box for the request    
    bbox = request.GET['bbox'].split(',')
    poly = Polygon.from_bbox(bbox)
    
    # Get the interest categories
    cats = request.GET['cat'].split(',')[:-1]
    cats = [int(cat_id) for cat_id in cats]

    # Fetch the restaurants
    restaurants = Restaurant.objects.filter(pt__within=poly,    
                                            categories__pk__in=cats)
    restaurants = list(set(restaurants))    # Remove duplicate items 
    
    # Convert to GeoJSON
    geojson_dict = {
            "type": "FeatureCollection",
            "features": [restaurant_to_json(restaurant) for restaurant in restaurants]
    }
    
    # Return the response
    return HttpResponse(json.dumps(geojson_dict), 
                        content_type="application/json")


"""
    Return a list of restaurants in range
"""  
def restaurant_near(request):
    # Figure out the request location
    point = get_location(request)
    
    # Find all restaurants within 3km from point
    restaurants = list(Restaurant.objects.filter(pt__distance_lte=(point, D(km=3))) \
                    .distance(point).order_by('distance'))
    
    # Make restaurant list together with distance    
    geojson_dict = make_result(point, restaurants)
    return HttpResponse(json.dumps(geojson_dict), 
                        content_type="application/json")
    

"""
    Return a list of restaurants matching a name pattern
"""  
def restaurant_search(request):
    point = get_location(request)
        
    pattern = request.GET['name']
    restaurants = Restaurant.objects.filter(name__icontains=pattern);
            
    geojson_dict = make_result(point, restaurants)
    return HttpResponse(json.dumps(geojson_dict), 
                        content_type="application/json")


"""  
    Figure out the request location
"""    
def get_location(request):
    location = map(float, request.GET['location'].split(','))
    point = Point(location)
    return point


"""
    Return list of restaurants together with distance to current location,
    ordered by distance
"""
def make_result(point, restaurants):
    result = [(distance(restaurant.pt, point), restaurant) for 
        restaurant in restaurants]
    result.sort(reverse=True)
    geojson_dict = {
        "type":"FeatureCollection", 
        "features":[restaurant_to_json(restaurant, dist) for 
            (dist, restaurant) in result]}
    return geojson_dict

    
"""
    Helper method that return corresponding json format for a restaurant
"""    
def restaurant_to_json(restaurant, distance=0):    
    geojson = {            
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [restaurant.pt.x, restaurant.pt.y]
            },
            "properties": {
                "name": restaurant.name,
                "address": restaurant.address,
                "phone": restaurant.phone,
                "website": restaurant.website,
                "email": restaurant.email,
                "description": restaurant.description.encode('ascii','ignore'),
                "cat_layer": list(restaurant.categories.all()).pop().name,
                "image": restaurant.img,
            },
            "id": restaurant.id
    }
    if distance != 0:
        geojson["properties"]["distance"] = "%.0f m" % D(km=distance).m
        
    return geojson