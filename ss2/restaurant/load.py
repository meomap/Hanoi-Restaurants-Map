'''
Created on May 23, 2012

@author: meo map
'''
from HTMLParser import HTMLParser
import urllib
from selenium import webdriver
from restaurant.models import Restaurant, Category
from django.contrib.gis.geos import Point
import unicode_handle

"""
    Parser to extract list of restaurants
"""
class ListPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.record = False
        self.restaurants = {}
        self.url = None
    
    def handle_starttag(self, tag, attrs):            
        if tag == 'a':
            for name, val in attrs:
                if name == 'class' and val == 'new-box-title':                    
                    self.record = True
        
        if self.record:           
            for name, val in attrs:
                if name == 'href':
                    if val.startswith("/vredir"):
                        val = "http://tnhvietnam.xemzi.com" + val   # partial link handle                  
                    self.url = val
        
    def handle_data(self, data):
        # Encode unicode character
        data = data.decode("utf-8").encode("ascii", "ignore")                   
        if self.record:
            # {name: {link: '...'}}
            self.restaurants[data] = {"link": self.url}
            self.record = False
            
    def handle_comment(self, data):
        #print "comment: " + data
        None
        
    def handle_endtag(self, tag):
        None
        
    def getList(self):
        return self.restaurants
    
    
def extractInfo(driver, attrs):
    metaFields = ["latitude", "longitude", "image", "description"]   
    addressFields = ["street-address", "locality", "country-name"]  # special handling for address
    styleFields = {".tel" : "phone", ".email": "email", ".url": "website"}    
    
    metas = driver.find_elements_by_tag_name('meta')     # Necessary info nested in meta tag
    for tag in metas:
        content = unicode_handle.unicodeToString(tag.get_attribute("content"))
        
        # Check meta tag to get categories
        if tag.get_attribute("name") == "keywords":
            categories = content[content.find("Restaurants")+12:] # Catch useful text
            categories = categories.strip()
            if len(categories) > 0:
                attrs['categories'] = categories.split(",") 
        
        # Check meta tag to get specific properties
        propName = str(tag.get_attribute("property"))[3:] # remove 'og:'
        if propName in metaFields:
            attrs[propName] =  content
    
        # Extract address
        elif propName in addressFields:
            attrs['address'].append(content)
    
    # Check tag with specific style
    for style in styleFields.keys():
        try:
            tag = driver.find_element_by_css_selector(style)
            if tag != None:
                propName = styleFields[style]
                attrs[propName] =  str(tag.text)
        except:
            pass
    
    print str(attrs)

def populateDB(restaurants):
    for name, properties in restaurants.iteritems():
        # Extract dictionary
        address = ", ".join(properties['address'])
        description = properties['description']
        
        phone = properties['phone']
        website = properties['website']
        email = properties['email']        
        
        loc = (float(properties['longitude']), float(properties['latitude']))
        
        # get image name only
        img = properties['image'].split('/')[-1].strip()
        
        categories = properties['categories']
        
        try:
            # Only add new restaurant
            Restaurant.objects.all().get(name=name)
        except: 
            # Create object in database
            r = Restaurant(name=name, address=address, description=description, 
                           phone=phone, website=website, email=email, img=img, 
                           pt=Point(loc))            
            r.save()
            print r
            
            i = 0
            while i < len(categories) and i < 2:
                catName = categories[i]
                catName = catName.upper()
                c = None
                try:
                    # Get existing category if exists
                    c = Category.objects.get(name=catName)
                except:
                    # Create new category
                    if i == 0:
                        c = Category(name=catName)  # First cat
                    else:
                        c = Category(name=catName, 
                                     super_cat=categories[0].upper())  # Sub cat
                    c.save()
                    print c
                r.categories.add(c)
                r.save()
                i += 1
         
def extractList(driver, restaurants):
    linkTags = driver.find_elements_by_tag_name("a")
    for tag in linkTags:
        if tag.get_attribute("class") == "new-box-title":
            name = tag.text.decode("utf-8").encode("ascii", "ignore")  
            url = tag.get_attribute("href")
            if url.startswith("/vredir"):
                url = "http://tnhvietnam.xemzi.com" + url   # partial link handle
            restaurants[name] = {'link': url} 
            print "(%s, %s)" %(name, url)
#______________________ MAIN __________________________________________
# pages 1 - 59
url = "http://tnhvietnam.xemzi.com/en/c/1/cat/11/nha-hang-hanoi#1/11"
restaurants = {}
driver = webdriver.Firefox()

print "Extract restaurant list ..."
try:
    driver.get(url)
    for i in range(20, 23):    
        # simulate click to jump page    
        script = 'javascript:updateCategoryResults({"category":"11","page":%s})' %(str(i))   
        driver.execute_script(script)
        print script
        driver.refresh()
        extractList(driver, restaurants)
   
finally:
    None

print(str(restaurants))    
print "--------------------"


#__ Extract restaurant info __
try:
    for name, attrs in restaurants.iteritems():    
        print "Extract info for ", name
        attrs['address'] = []
        attrs['website'] = ""
        attrs['phone'] = ""
        attrs['email'] = ""
        attrs['image'] = ""
        url = attrs['link']
        driver.get(url)
        extractInfo(driver, attrs)        
finally:
    driver.close()

print "--------------------"

print str(restaurants)

print "Populating database..."
#___ Populate database ___
populateDB(restaurants)
