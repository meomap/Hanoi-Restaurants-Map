'''
Created on May 27, 2012
    Export restaurants database to json format
@author: meo map
'''
from django.core import serializers
from restaurant.models import Restaurant, Category

json_out = open("C:\Documents and Settings\meo map\hellios\\restaurants.json", "w")
objs = list(Category.objects.all()) + list(Restaurant.objects.all())
serializers.serialize("json", objs, use_natural_keys=True, stream=json_out)
json_out.close()