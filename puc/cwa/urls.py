from django.conf.urls.defaults import *
from django.conf import settings
from puc.cwa import views



urlpatterns = patterns('',
    # Example:
    # (r'^puc/', include('puc.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^/?$', views.index),
    (r'^teste/widget/?$', views.widget),
    (r'^teste/chart/?$', views.chart),
    (r'^teste/chart2/?$', views.chart2),
    (r'^teste/chart-scroll/?$', views.chart_scroll),
    (r'^teste/resize/?$', views.resize),
)

import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
