# coding=utf-8
import datetime
import os

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from puc import templates
from puc.sme.models import Produto, Alarme, Monitor
from puc.sme.core.repository.produto_repository import ProdutoRepository
from puc.sme.core.repository.monitor_repository import MonitorRepository
from puc.sme.core.repository.alarme_repository import AlarmeRepository
from puc.core import json

#inicializacao dos repositorios
produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()

def index(request):
	"""Pagina principal da aplicacao por gerar relatorio"""
	produtos = produto_repository.get_produtos()
	alarmes = None
	monitores = None
	produtos_alarmes = produto_repository.get_produto_alarme_xref()
	alarmes_monitores = alarme_repository.get_alarme_monitor_xref()

	produtos_alarmes = json.encode_json(produtos_alarmes)
	alarmes_monitores = json.encode_json(alarmes_monitores)

	#pego atributos do get
	produto_id = request.POST.get('produto',None)
	alarme_id = request.POST.get('alarme',None)
	monitor_id = request.POST.get('monitor',None)
	data_inicio_str = request.POST.get('data_inicio',None)
	data_fim_str = request.POST.get('data_fim',None)
	print 'POST: %s' % request.POST
	
	gerar_relatorio = False
	erro = True
	#request GET
	if request.method == 'GET':
		erro = False
	
	#request POST
	if request.method == 'POST' :
		if (produto_id):
			alarmes = alarme_repository.get_alarmes_por_produto_id(produto_id)
		if (alarme_id):
			monitores = monitor_repository.get_monitor_por_alarme_id(alarme_id)

		#se todos os campos preenchidos habilito a geracao do relatorio
		if (int(produto_id) > 0 and int(alarme_id) > 0 and int(monitor_id) > 0 and len(data_inicio_str) > 0 and len(data_fim_str) > 0):
			gerar_relatorio = True
			erro = False

	
	return render_to_response(templates.TEMPLATE_RELATORIO_INDEX, { 
		'produtos': produtos,
		'alarmes' : alarmes,
		'monitores' : monitores,
		'erro' : erro,
		'gerar_relatorio' : gerar_relatorio,
		'request' : request,
		'produtos_alarmes' : produtos_alarmes,
		'alarmes_monitores' : alarmes_monitores})


def configurar_relatorio():
	"""configura relatorio"""
	html = """
	<h2>configura relatorio</h2>
	"""
	return HttpResponse(html)
