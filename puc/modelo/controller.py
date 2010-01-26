# coding=utf-8
from puc.core.controller import Controller

from traceback import *
import sys
import copy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from puc import templates
from puc.core import json
from puc.modelo.models import Modelo, VisaoRelatorio, VisaoHierarquica, Widget, TemplateModelo
from puc.modelo.repository import ModeloRepository, WidgetRepository, TemplateModeloRepository

modelo_repository = ModeloRepository()
template_repository = TemplateModeloRepository()
TEMPLATE_CSS_BASE = settings.BASE_DIR + '/media/css/modelo/template_base.css'

class ModeloController(Controller):
	
	def ver_template(self, template_id):
		"""retorna o template id"""
		template = template_repository.get_template_por_id(template_id)
		if template: 
			template_html = templates.MODELO_TEMPLATE_PATH + '/' + template.nome_arquivo_html
		
			print '### template(%s): %s' %(template_id, template)
			print '### template html(%s): %s' %(template_id, template_html)
		
			return render_to_response(template_html, { 'template' : template })
		else:
			output_html = """
			<center>
				<h2>Erro 500!</h2>
				<h3>Template id %s nao encontrado</h3><br>
			</center>
			""" % template_id
			return HttpResponseServerError(output_html)
			
	def ver_template_css(self, template_id):
		"""retorna o css do template id"""
		template = template_repository.get_template_por_id(template_id)
		if template: 
			template_html = templates.MODELO_TEMPLATE_PATH + '/' + template.nome_arquivo_html
			template_css = settings.BASE_DIR + '/media/css/modelo/' + template.nome_arquivo_css
			
			file_conteudo_css_base = open(TEMPLATE_CSS_BASE, 'r')
			file_conteudo_css_template = open(template_css, 'r')
			conteudo_css = file_conteudo_css_base.read() + '\n' + file_conteudo_css_template.read()
			
			#print conteudo_css
			print '### template(%s): %s' %(template_id, template)
			print '### template css base(%s): %s' %(template_id, TEMPLATE_CSS_BASE)
			
			return HttpResponse(conteudo_css, mimetype="text/css")

		else:
			conteudo_css = """/* Erro ao ler o css do Template id %s */"""  % template_id
			return HttpResponse(conteudo_css, mimetype="text/css")