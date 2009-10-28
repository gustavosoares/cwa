from django.conf.urls.defaults import *
from django.conf import settings
from puc.relatorio import views



urlpatterns = patterns('',
    # Example:
    # (r'^puc/', include('puc.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^controller/?$', views.controller),
    (r'^/?$', views.index),
    (r'^grafico/?$', views.index_grafico),
    (r'^xml/?$', views.get_xml),

)

import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
