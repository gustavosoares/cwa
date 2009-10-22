# coding=utf-8
from traceback import *
import sys
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

def index(request):
	return listar_produto_alarme(request)
	
def listar_produto(request):
	"""retorna a listagem dos produtos no sme2"""
	return HttpResponse("<h1>página velha</h1>")

def listar_produto_alarme(request):
	"""controller: listagem dos produtos e os alarmes"""
	produtos = produto_repository.get_produtos_alarmando()
	#print produtos
	#print '-' * 50
	produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
	#print produtos_alarmes
	return render_to_response(templates.TEMPLATE_LISTAR_PRODUTO_ALARME, 
					{ 'produtos' : produtos,
					'produtos_alarmes' : produtos_alarmes,
	 				'colors' : util.colors})

def listar_monitor_do_alarme(request, alm_id=None):
	"""lista monitores alarmando do alarme id"""
	monitores = monitor_repository.get_monitor_alarmando_por_alarme_id(alm_id)
	alarme = alarme_repository.get_alarme_por_id(alm_id)
	produto = produto_repository.get_produto_por_id(alarme.prd_id)

	return render_to_response(templates.TEMPLATE_LISTAR_MONITOR_DO_ALARME, 
					{ 'monitores' : monitores,
					'alarme' : alarme,
					'produto' : produto,
	 				'colors' : util.colors})

def ver_evento(request, mon_id=None):
	"""visualiza os eventos do monitor passado como parametro	"""
	eventos = monitor_repository.get_eventos_por_monitor_id(mon_id)
	monitor = monitor_repository.get_monitor_por_id(mon_id)
	alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
	produto = produto_repository.get_produto_por_id(alarme.prd_id)
	colunas_desc = eventos[0].descricao_colunas

	rel = relatorio_factory.RelatorioFactory().get_relatorio('tabular')
	rel.produto = produto
	rel.alarme = alarme
	rel.monitor = monitor
	rel.eventos = eventos
	rel.descricao_colunas = colunas_desc
	
	return render_to_response(templates.TEMPLATE_VER_EVENTO, 
					{ 'relatorio' : rel,
	 				'colors' : util.colors})
	
def fechar_evento(request, mon_id=None, pad_id=None):
	"""fecha o evento do monitor passado como parametro"""
	monitor = monitor_repository.get_monitor_por_id(mon_id)
	alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
	produto = produto_repository.get_produto_por_id(alarme.prd_id)
	try:
		msg = '''fechar evento %s do monitor %s''' % (pad_id, mon_id)
		print msg
		monitor_repository.fechar_evento(pad_id, monitor, alarme, produto)
		return HttpResponseRedirect('/sme2/evento/monitor/%s' % mon_id)
	except Exception, e:
		print_exc(file=sys.stdout)
		msg = 'Erro ao fechar o evento %s: %s' % (pad_id, e)
		print msg
		html = '<h1>erro 500!!!</h1></br></br><h2>Erro ao fechar o evento %s</h2>' % (pad_id)
		return HttpResponseServerError(html)

def fechar_todos_eventos(request, mon_id=None):
	"""fechar_todos_eventos do monitor id"""
	monitor = monitor_repository.get_monitor_por_id(mon_id)
	alarme = alarme_repository.get_alarme_por_id(monitor.alm_id)
	produto = produto_repository.get_produto_por_id(alarme.prd_id)
	monitor_repository.fechar_todos_eventos(monitor, alarme, produto)
	return HttpResponseRedirect('/sme2/evento/monitor/%s' % mon_id)

