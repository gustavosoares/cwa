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

from puc import templates
from puc.sme.models import Produto, Alarme, Monitor
from puc.sme.core.repository.produto_repository import ProdutoRepository
from puc.sme.core.repository.monitor_repository import MonitorRepository
from puc.sme.core.repository.alarme_repository import AlarmeRepository
from puc.sme.core import domain
from puc.sme2.core import util
from puc.relatorio.core import factory as relatorio_factory

produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()

#print 'id produto_repository: %s' % id(produto_repository)
#print 'id alarme_repository: %s' % id(alarme_repository)
#print 'id monitor_repository: %s' % id(monitor_repository)

class Sme2Controller(Controller):
	
	def index(self):
		return self.listar_produto_alarme_monitor()

	def admin(self):
		"""retorna o admin no sme2"""
		return HttpResponse("<h1>Admin SME2</h1>")

	def listar_produto(self):
		"""retorna a listagem dos produtos no sme2"""
		return HttpResponse("<h1>página velha</h1>")

	def listar_produto_alarme(self):
		"""controller: listagem dos produtos e os alarmes"""

		produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()

		return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO_ALARME, 
						{ 'produtos' : None,
						'produtos_alarmes' : produtos_alarmes,
		 				'colors' : util.colors})


	def listar_produto_alarme_monitor(self):
		"""controller: listagem dos produtos, alarme e monitores"""

		produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()

		return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO_ALARME_MONITOR, 
						{ 'produtos' : None,
						'produtos_alarmes' : produtos_alarmes,
		 				'colors' : util.colors})

	def listar_monitor_do_alarme(self, alm_id=None):
		"""lista monitores alarmando do alarme id"""
		monitores = monitor_repository.get_monitor_alarmando_por_alarme_id(alm_id)
		alarme = alarme_repository.get_alarme_por_id(alm_id)
		produto = produto_repository.get_produto_por_id(alarme.prd_id)

		return render_to_response(templates.TEMPLATE_LISTAR_MONITOR_DO_ALARME, 
						{ 'monitores' : monitores,
						'alarme' : alarme,
						'produto' : produto,
		 				'colors' : util.colors})

	def ver_evento(self, mon_id=None):
		"""visualiza os eventos do monitor passado como parametro"""

		eventos = monitor_repository.get_eventos_por_monitor_id(mon_id)
		monitor = monitor_repository.get_monitor_por_id(mon_id)
		alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
		produto = produto_repository.get_produto_por_id(alarme.prd_id)
		if len(eventos) > 0:
			colunas_desc = eventos[0].descricao_colunas
			print '\n\nmetadados: %s\n' % eventos[0].metadados
			print '\ncolunas desc: %s\n' % eventos[0].descricao_colunas

			rel = relatorio_factory.RelatorioFactory().get_relatorio('tabular')
			rel.produto = produto
			rel.alarme = alarme
			rel.monitor = monitor
			rel.eventos = eventos
			rel.descricao_colunas = colunas_desc

			return render_to_response(templates.TEMPLATE_VER_EVENTO, 
							{ 'relatorio' : rel,
			 				'colors' : util.colors})
		else:
			#retorno para a pagina do alarme, pois nao tem mais nenhum evento
			#return HttpResponseRedirect('/sme2/monitor/alarme/%s' % alarme.alm_id)
			return HttpResponseRedirect('/sme2/')

	def fechar_evento(self, mon_id=None, pad_id=None):
		"""fecha o evento do monitor passado como parametro"""
		monitor = monitor_repository.get_monitor_por_id(mon_id)
		alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
		produto = produto_repository.get_produto_por_id(alarme.prd_id)
		try:
			msg = '''fechar evento %s do monitor %s''' % (pad_id, mon_id)
			print msg
			monitor_repository.fechar_evento(pad_id, monitor, alarme, produto)
			#eventos = monitor_repository.get_eventos_por_monitor_id(mon_id)
			return HttpResponseRedirect('/sme2/evento/monitor/%s' % mon_id)
		except Exception, e:
			print_exc(file=sys.stdout)
			msg = 'Erro ao fechar o evento %s: %s' % (pad_id, e)
			print msg
			html = '<h1>erro 500!!!</h1></br></br><h2>Erro ao fechar o evento %s</h2>' % (pad_id)
			return HttpResponseServerError(html)

	def fechar_todos_eventos(self, mon_id=None):
		"""fechar_todos_eventos do monitor id"""
		monitor = monitor_repository.get_monitor_por_id(mon_id)
		alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
		produto = produto_repository.get_produto_por_id(alarme.prd_id)
		try:
			msg = '''fechando TODOS os eventos do monitor %s''' % (mon_id)
			print msg
			monitor_repository.fechar_todos_eventos(monitor, alarme, produto)
			#eventos = monitor_repository.get_eventos_por_monitor_id(mon_id)
			return HttpResponseRedirect('/sme2/')
		except Exception, e:
			print_exc(file=sys.stdout)
			msg = 'Erro ao fechar TODOS os eventos do monitor %s: %s' % (mon_id, e)
			print msg
			html = '<h1>erro 500!!!</h1></br></br><h2>Erro ao fechar todos os eventos do monitor %s(%s)</h2>' % (monitor.mon_nome, monitor.mon_id)
			return HttpResponseServerError(html)
