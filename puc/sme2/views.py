# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
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

def listar_produto(request):
	"""retorna a listagem dos produtos no sme2"""
	produtos = produto_repository.get_produtos_alarmando()
	produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
	print produtos_alarmes
	return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO, 
					{ 'produtos' : produtos,
					'produtos_alarmes' : produtos_alarmes,
	 				'colors' : util.colors})

def listar_produto_alarme(request):
	"""controller: listagem dos produtos e os alarmes"""
	produtos = produto_repository.get_produtos_alarmando()
	produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
	print produtos_alarmes
	return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO_ALARME, 
					{ 'produtos' : produtos,
					'produtos_alarmes' : produtos_alarmes,
	 				'colors' : util.colors})

def listar_monitor_do_alarme(request, alm_id=None):
	"""lista monitores alarmando do alarme id"""
	monitores = monitor_repository.get_monitor_alarmando_por_alarme_id(alm_id)
	alarme = alarme_repository.get_alarme_por_id(alm_id)
	print monitores
	print alarme
	return render_to_response(templates.TEMPLATE_LISTAR_MONITOR_DO_ALARME, 
					{ 'monitores' : monitores,
					'alarme' : alarme,
	 				'colors' : util.colors})

def ver_evento(request, mon_id=None):
	"""visualiza os eventos do monitor passado como parametro	"""
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
	
def fechar_evento(request, mon_id=None, pad_id=None):
	"""fecha o evento do monitor passado como parametro"""
	monitor = monitor_repository.get_monitor_por_id(mon_id)
	alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
	produto = produto_repository.get_produto_por_id(alarme.prd_id)
	try:
		#monitor.fechar_evento(pad_id, monitor, alarme, produto)
		msg = '''fechar evento %s do monitor %s</h1>''' % (pad_id, mon_id)
		print msg
		return HttpResponseRedirect('/sme2/evento/monitor/%s' % mon_id)
	except Exception, e:
		msg = 'Erro ao fechar o evento %s: %s' % (pad_id, e)
		raise HttpResponseServerError(msg)
		

