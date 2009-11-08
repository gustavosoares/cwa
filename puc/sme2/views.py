# coding=utf-8
from puc.sme2.core.controller import Sme2Controller

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
	return sme2_controller.listar_produto_alarme_monitor()

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
	


