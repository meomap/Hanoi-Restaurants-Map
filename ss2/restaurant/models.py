from django.contrib.gis.db import models

class CategoryManager(models.Manager):
    def get_by_natural_key(self, name, super_cat):
        return self.get(name=name, super_cat=super_cat)

class Category(models.Model):
    name = models.CharField(max_length=50)
    super_cat = models.CharField(max_length=50, default="")
    
    objects = CategoryManager() # Override default object for natural key    

    def natural_key(self):
        return (self.name, self.super_cat)

    class Meta:
        unique_together = (('name', 'super_cat'),)

    def __unicode__(self):
        return self.name
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(null=True)    
    
    phone = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=50, null=True)
    img = models.CharField(max_length=20, null=True)
     
    categories = models.ManyToManyField(Category)   # Many-to-many reference
    
    pt = models.PointField()
    
    objects = models.GeoManager()   # Override default object type
    
    def __unicode__(self):
        return "(%s, %s, %s, %s)"  % (self.name, self.phone, self.address, str(self.pt)) 