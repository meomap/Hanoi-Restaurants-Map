from django.contrib.gis.db import models

# Create your models here.
class Vertex(models.Model):
    id = models.IntegerField(primary_key=True)
    
    pt = models.PointField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "%s, %s" % (self.id, str(self.pt))  
    
    
class Edge(models.Model):
    cost = models.FloatField()      # path cost
    name = models.CharField(max_length=100)    
    reverse = models.BooleanField()
    
    vertex_start = models.ForeignKey(Vertex, related_name="start_edge")
    vertex_end = models.ForeignKey(Vertex, related_name="end_edge")
    
    line = models.LineStringField()
    
    objects = models.GeoManager()