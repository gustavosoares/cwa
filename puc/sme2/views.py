# coding=utf-8
from puc.sme2.core.controller import Sme2Controller

'''
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
'''
#print 'id produto_repository: %s' % id(produto_repository)
#print 'id alarme_repository: %s' % id(alarme_repository)
#print 'id monitor_repository: %s' % id(monitor_repository)

def index(request):
	#return listar_produto_alarme(request)
	sme2_controller = Sme2Controller(request)
	return sme2_controller.index()


def listar_produto(request):
	"""retorna a listagem dos produtos no sme2"""
	sme2_controller = Sme2Controller(request)
	return sme2_controller.listar_produto()


def listar_produto_alarme(request):
	"""controller: listagem dos produtos e os alarmes"""
	sme2_controller = Sme2Controller(request)
	return sme2_controller.listar_produto_alarme()

def listar_produto_alarme_monitor(request):
	"""controller: listagem dos produtos, alarme e monitores"""
	
	sme2_controller = Sme2Controller(request)
	sme2_controller.listar_produto_alarme_monitor()


def listar_monitor_do_alarme(request, alm_id=None):
	"""lista monitores alarmando do alarme id"""
	
	sme2_controller = Sme2Controller(request)
	return sme2_controller.listar_monitor_do_alarme(alm_id)


def ver_evento(request, mon_id=None):
	"""visualiza os eventos do monitor passado como parametro"""
	
	sme2_controller = Sme2Controller(request)
	return sme2_controller.ver_evento(mon_id)

	
def fechar_evento(request, mon_id=None, pad_id=None):
	"""fecha o evento do monitor passado como parametro"""
	
	sme2_controller = Sme2Controller(request)
	return sme2_controller.fechar_evento(mon_id, pad_id)


def fechar_todos_eventos(request, mon_id=None):
	"""fechar_todos_eventos do monitor id"""
	
	sme2_controller = Sme2Controller(request)
	return sme2_controller.fechar_todos_eventos(mon_id)
	


