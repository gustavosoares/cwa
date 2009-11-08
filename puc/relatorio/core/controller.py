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
from puc.sme.models import Produto, Alarme, Monitor
from puc.sme.core.repository.produto_repository import ProdutoRepository
from puc.sme.core.repository.monitor_repository import MonitorRepository
from puc.sme.core.repository.alarme_repository import AlarmeRepository
from puc.modelo import repository
from puc.relatorio.core import domain
from puc.relatorio.core import factory
from puc.core import json
from puc.sme.core import domain
from puc.sme2.core import util

#inicializacao dos repositorios
produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()
visao_repository = repository.VisaoRepository()

class RelatorioController(Controller):

	def index(self):
		"""Pagina principal da aplicacao por gerar relatorio"""
		#declaracao de variaveis passadas para o template
		produtos = produto_repository.get_produtos()
		alarmes = None
		monitores = None
		relatorio = None

		produtos_alarmes = produto_repository.get_produto_alarme_xref()
		alarmes_monitores = alarme_repository.get_alarme_monitor_xref()
		#gero objeto json para ser usado no carregamento da lista
		produtos_alarmes = json.encode_json(produtos_alarmes)
		alarmes_monitores = json.encode_json(alarmes_monitores)

		#pego atributos do POST
		produto_id = self.request.POST.get('produto',None)
		alarme_id = self.request.POST.get('alarme',None)
		monitor_id = self.request.POST.get('monitor',None)
		data_inicio_str = self.request.POST.get('data_inicio',None)
		data_fim_str = self.request.POST.get('data_fim',None)
		print '[RELATORIO] POST: %s' % self.request.POST

		erro = True
		#request GET
		if self.request.method == 'GET':
			erro = False

		#request POST
		if self.request.method == 'POST' :
			if (produto_id):
				alarmes = alarme_repository.get_alarmes_por_produto_id(produto_id)
			if (alarme_id):
				monitores = monitor_repository.get_monitores_por_alarme_id(alarme_id)

			#se todos os campos preenchidos gero o relatorio
			if (int(produto_id) > 0 and int(alarme_id) > 0 and int(monitor_id) > 0 and len(data_inicio_str) > 0 and len(data_fim_str) > 0):
				erro = False

				#adiciono os parametros do post no get
				self.request.GET = self.request.POST

				#obtenho os eventos para o monitor em questao no intervalo definido
				monitor = monitor_repository.get_monitor_por_id(monitor_id)
				alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
				produto = produto_repository.get_produto_por_id(alarme.prd_id)
				eventos = monitor_repository.get_eventos_por_periodo_por_monitor_id(monitor_id, data_inicio_str, data_fim_str)
				count_eventos = len(eventos)
				print 'Total de eventos: %s' % count_eventos
				if count_eventos > 0:
					colunas_desc = eventos[0].descricao_colunas
				else:
					colunas_desc = []

				#valida o tipo de relatorio a ser gerado
				relatorio = factory.RelatorioFactory().get_relatorio_automaticamente()
				print '###relatorio: %s' % (type(relatorio))
				relatorio.produto = produto
				relatorio.alarme = alarme
				relatorio.monitor = monitor
				relatorio.eventos = eventos
				relatorio.descricao_colunas = colunas_desc

				grafico = relatorio.grafico
				if grafico: #relatorio tabular nao tem grafico
					print '###grafico: %s' % (type(grafico))
					grafico.produto_id = produto_id
					grafico.alarme_id = alarme_id
					grafico.monitor_id = monitor_id
					grafico.data_inicio = data_inicio_str
					grafico.data_fim = data_fim_str


		return render_to_response(templates.TEMPLATE_RELATORIO_INDEX, {
			'produtos_alarmes' : produtos_alarmes,
			'alarmes_monitores' : alarmes_monitores,
			'produtos': produtos,
			'alarmes' : alarmes,
			'monitores' : monitores,
			'erro' : erro,
			'relatorio' : relatorio,
			'request' : self.request})

	def get_xml(self):
		"""
		retorna o xml para ser gerado pelo framework em flash de geracao de graficos
		Exemplo de request: http://localhost:10000/relatorio/xml?produto=35&alarme=125&monitor=396&data_inicio=2009-08-01&data_fim=2009-10-28
		"""
		print '[XML] GET: %s' % self.request.GET

		relatorio = None
		#pego atributos do POST
		produto_id = self.request.GET.get('produto',None)
		alarme_id = self.request.GET.get('alarme',None)
		monitor_id = self.request.GET.get('monitor',None)
		data_inicio_str = self.request.GET.get('data_inicio',None)
		data_fim_str = self.request.GET.get('data_fim',None)

		if (int(produto_id) > 0 and int(alarme_id) > 0 and int(monitor_id) > 0 and len(data_inicio_str) > 0 and len(data_fim_str) > 0):
			#obtenho os eventos para o monitor em questao no intervalo definido
			monitor = monitor_repository.get_monitor_por_id(monitor_id)
			alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
			produto = produto_repository.get_produto_por_id(alarme.prd_id)
			eventos = monitor_repository.get_eventos_por_periodo_por_monitor_id(monitor_id, data_inicio_str, data_fim_str)
			count_eventos = len(eventos)
			print 'Total de eventos: %s' % count_eventos
			if count_eventos > 0:
				colunas_desc = eventos[0].descricao_colunas
			else:
				colunas_desc = []

			relatorio = factory.RelatorioFactory().get_relatorio_automaticamente()
			print '###relatorio: %s' % (type(relatorio))
			relatorio.produto = produto
			relatorio.alarme = alarme
			relatorio.monitor = monitor
			relatorio.eventos = eventos

			relatorio.descricao_colunas = colunas_desc
			assert relatorio != None, 'tipo de relatorio desconhecido'
			grafico = relatorio.grafico
			print '###grafico: %s' % (type(grafico))
			xml = relatorio.get_xml()

			print 'valor maximo: %s' % grafico.valor_maximo

			return HttpResponse(xml, mimetype="application/xml")
		else:
			print 'erro na geracao do xml'
			return HttpResponse(status=500)	