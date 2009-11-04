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
from puc.modelo.repository import ModeloRepository
from puc.core import json

modelo_repository = ModeloRepository()

def index(request):
	"""Pagina princiap da aplicacao cwa"""
	
	modelo = modelo_repository.get_modelo_ativo()
	print '[CWA INDEX] modelo ativo: %s' % modelo
	
	modelo_settings_json = modelo_repository.get_modelo_settings(modelo.nome)
	print '[CWA INDEX] modelo settings: %s' % modelo_settings_json
	#pego as informacoes do modelo configurado
	return render_to_response(templates.TEMPLATE_CWA_INDEX, { 'settings' : modelo_settings_json})

	
def widget(request):
	return render_to_response('cwa/_teste/teste_widget.html')

def chart(request):
	return render_to_response('cwa/_teste/teste_chart.html')

def chart2(request):
	return render_to_response('cwa/_teste/teste_chart2.html')	

def resize(request):
	return render_to_response('cwa/_teste/teste_resize.html')
	
def chart_scroll(request):
	return render_to_response('cwa/_teste/teste_chart_scroll.html')