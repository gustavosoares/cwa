from django.conf.urls.defaults import *
from django.conf import settings
from puc.sme2 import views



urlpatterns = patterns('',
    # Example:
    # (r'^puc/', include('puc.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^controller/?$', views.controller),
    (r'^/?$', views.listar_produto_alarme),
    (r'^produto/?$', views.listar_produto),
    #retorna lista de monitores do alarme id
    (r'^alarme/(?P<alm_id>\d+)/?$', views.listar_monitor_do_alarme),
    (r'^monitor/(?P<mon_id>\d+)/?$', views.ver_monitor),

)

import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
