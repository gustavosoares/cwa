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
    (r'^/?$', views.index),
    (r'^admin/?$', views.admin),
    (r'^produto/?$', views.listar_produto),
    #monitores do alarme id
    (r'^monitor/alarme/(?P<alm_id>\d+)/?$', views.listar_monitor_do_alarme),
    #eventos do monitor id
    (r'^evento/monitor/(?P<mon_id>\d+)/?$', views.ver_evento),
    #fecha uma evento de um determinado monitor a partir do id do evento
    (r'^evento/fechar/(?P<mon_id>\d+)/(?P<pad_id>\d+)/?$', views.fechar_evento),
    #fecha todos os eventos para o monitor id
    #TODO
    (r'^evento/fechar/(?P<mon_id>\d+)/todos/?$', views.fechar_todos_eventos),

)

import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
