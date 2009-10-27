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
	modelo_settings = {}
	modelo = modelo_repository.get_modelo_por_nome(settings.MODELO)
	assert modelo != None, 'Modelo configurado nao existe no sistema!'
	metadado = modelo.metadado
	print 'metadado: %s' % metadado
	#Ex.:portal-column-0&portal-column-1:block-tabular&portal-column-bottom:block-relatorio
	colunas = metadado.split('&')
	for coluna in colunas:
		visoes = coluna.split(':')
		if len(visoes) > 1:
			container = visoes[0]
			visoes_aux = visoes[1:]
			print '%s ->> %s' % (container, visoes_aux)
			modelo_settings[container] = visoes_aux

	modelo_settings_json = json.encode_json(modelo_settings)
	print 'modelo settings: %s' % modelo_settings_json
	#pego as informacoes do modelo configurado
	return render_to_response(templates.TEMPLATE_CWA_INDEX, { 'settings' : modelo_settings_json})

	
def widget(request):
	return render_to_response('cwa/teste_widget.html')

def chart(request):
	return render_to_response('cwa/teste_chart.html')

def chart2(request):
	return render_to_response('cwa/teste_chart2.html')	

def resize(request):
	return render_to_response('cwa/teste_resize.html')