'''
Created on May 27, 2012
    Retrieve newly updated restaurants images and store in local folder
    Run this file after fetching restaurant info from the Internet
@author: meo map
'''
from restaurant.models import Restaurant
import urllib
import os

images = [item.img for item in Restaurant.objects.all()]
os.chdir(os.getcwd() + "/static/images/thumbs")
print "current working dir", os.getcwd()
print "Obtaining restaurant thumbnails ..."
for image in images:
    if len(image) > 0:        
        #os.chdir(os.getcwd() + "\\static\\images\\thumbs\\")
        if os.path.exists(image) == False:
            #http://tnhvietnam.xemzi.com/images/bizimages/cropped/9101.jpg
            link = "http://tnhvietnam.xemzi.com/images/bizimages/cropped/" + image;
            print link            
            u = urllib.urlopen(link)
            f = open(image, 'wb')
            f.write(u.read())
            f.close()
    
print "Done!"