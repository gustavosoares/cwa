# coding=utf-8
from puc.core.controller import Controller

import datetime
import os

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from puc import templates
from puc.modelo.repository import ModeloRepository, WidgetRepository
from puc.core import json

modelo_repository = ModeloRepository()
widget_repository = WidgetRepository()

class CwaController(Controller):

	def index(self):
		"""Pagina principal da aplicacao cwa"""

		modelo = modelo_repository.get_modelo_ativo()
		print '[CWA INDEX] modelo ativo: %s' % modelo
		
		widgets = widget_repository.get_todos()
		
		modelo_settings_json = modelo_repository.get_modelo_settings(modelo.nome)
		print '[CWA INDEX] modelo settings: %s' % modelo_settings_json
		#pego as informacoes do modelo configurado
		return render_to_response(templates.TEMPLATE_CWA_INDEX, { 'settings' : modelo_settings_json, 'my_widgets' : widgets})

	def widget(self):
		return render_to_response('cwa/_teste/teste_widget.html')

	def chart(self):
		return render_to_response('cwa/_teste/teste_chart.html')

	def chart2(self):
		return render_to_response('cwa/_teste/teste_chart2.html')	

	def resize(self):
		return render_to_response('cwa/_teste/teste_resize.html')

	def chart_scroll(self):
		return render_to_response('cwa/_teste/teste_chart_scroll.html')
