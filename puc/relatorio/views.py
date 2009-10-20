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
from puc.sme.core import domain
from puc.sme2.core import util

#inicializacao dos repositorios
produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()

def index(request):
	"""Pagina principal da aplicacao por gerar relatorio"""
	#declaracao de variaveis passadas para o template
	produtos = produto_repository.get_produtos()
	alarmes = None
	monitores = None
	produto = None
	alarme = None 
	monitor = None
	colunas_desc = None
	eventos = None
	produtos_alarmes = produto_repository.get_produto_alarme_xref()
	alarmes_monitores = alarme_repository.get_alarme_monitor_xref()

	produtos_alarmes = json.encode_json(produtos_alarmes)
	alarmes_monitores = json.encode_json(alarmes_monitores)

	#pego atributos do POST
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
			#valida o tipo de relatorio a ser gerado
			
			#obtenho os eventos para monitor em questao no intervalo definido
			rows, monitor, colunas_desc, colunas_nome = monitor_repository.get_eventos_por_periodo_por_monitor_id(monitor_id, data_inicio_str, data_fim_str)
			alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
			produto = produto_repository.get_produto_por_id(alarme.prd_id)
			#crio array de eventos
			eventos = []
			for row in rows:
				eventos.append(domain.Evento(monitor, alarme, row))

	
	return render_to_response(templates.TEMPLATE_RELATORIO_INDEX, { 
		'produtos': produtos,
		'alarmes' : alarmes,
		'monitores' : monitores,
		'produto' : produto,
		'alarme' : alarme,
		'monitor' : monitor,
		'colunas_desc' : colunas_desc,
		'eventos' : eventos,
		'erro' : erro,
		'gerar_relatorio' : gerar_relatorio,
		'request' : request,
		'colors' : util.colors,
		'produtos_alarmes' : produtos_alarmes,
		'alarmes_monitores' : alarmes_monitores})


def configurar_relatorio():
	"""configura relatorio"""
	html = """
	<h2>configura relatorio</h2>
	"""
	return HttpResponse(html)
