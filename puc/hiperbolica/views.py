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
	
	raiz = domain.NoHiperbolico()
	
	raiz.id = 0
	raiz.name = 'produto'
	
	h1 = domain.NoHiperbolico()
	h1.id = 1
	h1.name = 'gustavo'
	h1.dim = 7
	raiz.add_children(h1)
	
	print 'arvore: %s' % raiz

	arvore_json = raiz
	
	return render_to_response(templates.TEMPLATE_HIPERBOLICA_INDEX, {'arvore_json' : arvore_json})

def teste(request):
	"""pagina de teste da visualizacao hiperbolica"""

	return render_to_response("hiperbolica/teste.html", {})