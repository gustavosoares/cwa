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


def index(request):
	"""Pagina princial da aplicacao por gerar relatorio"""
	##return HttpResponse("relatorio")
	produtos = ProdutoRepository.get_produtos()
	alarmes = None
	monitores = None
	produtos_alarmes = ProdutoRepository.get_produto_alarme_xref()
	alarmes_monitores = AlarmeRepository.get_alarme_monitor_xref()

	produtos_alarmes = json.encode_json(produtos_alarmes)
	alarmes_monitores = json.encode_json(alarmes_monitores)


	#pego atributos do get
	produto_id = request.POST.get('produto',None)
	alarme_id = request.POST.get('alarme',None)
	monitor_id = request.POST.get('monitor',None)
	data_inicio_str = request.POST.get('data_inicio',None)
	data_fim_str = request.POST.get('data_fim',None)
	print 'POST: %s' % request.POST
	
	erro = False
	frm2 = False
	if (produto_id):
		ProdutoRepository.get_produto_id(produto_id)
	if (alarme_id):
		pass
	if (monitor_id):
		pass
		
	if (produto_id and alarme_id and monitor_id):
		frm2 = True
		print 'Produto id: %s' % produto_id
		print 'Alarme id: %s' % alarme_id
		print 'Monitor id: %s' % monitor_id
	else:
		erro = True
	
	return render_to_response(templates.TEMPLATE_RELATORIO_INDEX, { 
		'produtos': produtos,
		'produtos_alarmes' : produtos_alarmes,
		'alarmes_monitores' : alarmes_monitores})

def configurar_relatorio():
	"""configura relatorio"""
	html = """
	<h2>configura relatorio</h2>
	"""
	return HttpResponse(html)
