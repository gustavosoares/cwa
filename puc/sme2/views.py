# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from puc import templates
from puc.sme.models import Produto, Alarme, Monitor
from puc.sme.core.repository import produto_repository
from puc.sme.core.repository import monitor_repository
from puc.sme.core.repository import alarme_repository
from puc.sme.core import domain

from puc.sme2.core import util

#retorna a listagem dos produtos no sme2
def listar_produto(request):
	produtos = produto_repository.get_produtos_alarmando()
	produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
	print produtos_alarmes
	return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO, 
					{ 'produtos' : produtos,
					'produtos_alarmes' : produtos_alarmes,
	 				'colors' : util.colors})

#controller: listagem dos produtos e os alarmes
def listar_produto_alarme(request):
	produtos = produto_repository.get_produtos_alarmando()
	produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
	print produtos_alarmes
	return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO_ALARME, 
					{ 'produtos' : produtos,
					'produtos_alarmes' : produtos_alarmes,
	 				'colors' : util.colors})

#lista monitores do alarme id
def listar_monitor_do_alarme(request, alm_id=None):
	monitores = monitor_repository.get_monitor_por_alarme_id(alm_id)
	alarme = alarme_repository.get_alarme_por_id(alm_id)
	print monitores
	print alarme
	return render_to_response(templates.TEMPLATE_LISTAR_MONITOR_DO_ALARME, 
					{ 'monitores' : monitores,
					'alarme' : alarme,
	 				'colors' : util.colors})

#visualiza os eventos do monitor passado como parametro	
def ver_evento(request, mon_id=None):
	rows, monitor, colunas_desc, colunas_nome = monitor_repository.get_eventos_por_monitor_id(mon_id)
	alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
	#crio array de eventos
	eventos = []
	for row in rows:
		eventos.append(domain.Evento(monitor, alarme, row))

	return render_to_response(templates.TEMPLATE_VER_EVENTO, 
					{ 'monitor' : monitor,
					'alarme' : alarme,
					'colunas_desc' : colunas_desc,
					'eventos' : eventos,
	 				'colors' : util.colors})

#fecha o evento do monitor passado como parametro	
def fechar_evento(request, mon_id=None, pad_id=None):
	monitor = monitor_repository.get_monitor_por_id(mon_id)
	alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
	produto = produto_repository.get_produto_por_id(alarme.prd_id)
	
	html = '''
	<h1>fechar evento do monitor %s</h1>
	''' % mon_id
	
	return HttpResponse(html)
