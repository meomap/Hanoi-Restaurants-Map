'''
Created on May 27, 2012
    Export restaurants database to json format
@author: meo map
'''
from django.core import serializers
from route.models import Edge, Vertex

json_out = open("C:\Documents and Settings\meo map\hellios\\roads.json", "w")
objs = list(Vertex.objects.all()) + list(Edge.objects.all())
serializers.serialize("json", objs, stream=json_out)
json_out.close()