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
from puc.modelo import repository

from puc.hiperbolica.core import domain
#inicializacao dos repositorios
produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()
visao_repository = repository.VisaoRepository()

def index(request):
	"""pagina principal da visualizacao hiperbolica"""
	
	h = domain.NoHiperbolico()
	
	h.id = 1
	h.name = 'produto'
	
	print 'nó: %s' % h

	arvore_json = h
	
	return render_to_response(templates.TEMPLATE_HIPERBOLICA_INDEX, {'arvore_json' : arvore_json})

def teste(request):
	"""pagina de teste da visualizacao hiperbolica"""

	return render_to_response("hiperbolica/teste.html", {})