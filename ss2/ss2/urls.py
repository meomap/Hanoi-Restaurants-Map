from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ss2.views.home', name='home'),
    # url(r'^ss2/', include('ss2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
#    url(r'^restaurant$',
#        'django.views.generic.simple.direct_to_template',
#        {'template': 'restaurant.html'}
#    ),
    url(r'^restaurant$',
        'restaurant.views.index'
    ),
    url(r'^restaurant.json$', 'restaurant.views.restaurant_list'),
    url(r'^findnearby.json$', 'restaurant.views.restaurant_near'),
    url(r'^findrestaurants.json$', 'restaurant.views.restaurant_search'),
    url(r'^route.json$', 'route.views.search_route'),
)
