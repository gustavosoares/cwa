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


def index(request):
	"""Pagina princial da aplicacao por gerar relatorio"""
	##return HttpResponse("relatorio")
	produtos = ProdutoRepository.get_produtos()

	return render_to_response(templates.TEMPLATE_RELATORIO_INDEX, { 
		'produtos': produtos})
