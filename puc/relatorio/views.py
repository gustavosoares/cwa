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
	alarmes = AlarmeRepository.get_alarmes()
	produtos_alarmes = {}
	for alarme in alarmes:
		l = produtos_alarmes.get(alarme.prd_id,[])
		l.append({'alm_nome' : alarme.alm_nome, 'alm_id' : alarme.alm_id})
		produtos_alarmes[alarme.prd_id] = l
		
	monitores = MonitorRepository.get_monitores()
	alarmes_monitores = {}
	for monitor in monitores:
		l = alarmes_monitores.get(monitor.alm_id,[])
		l.append({'mon_nome' : monitor.mon_nome, 'mon_id' : monitor.mon_id})
		alarmes_monitores[monitor.alm_id] = l
	
	alarmes = None
	monitores = None
	produtos_alarmes = json.encode_json(produtos_alarmes)
	alarmes_monitores = json.encode_json(alarmes_monitores)

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
