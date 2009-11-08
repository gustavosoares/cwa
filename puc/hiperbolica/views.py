# coding=utf-8
from puc.hiperbolica.core.controller import HiperbolicaController

def index(request):
	"""pagina principal da visualizacao hiperbolica"""
	h_controller = HiperbolicaController(request)
	return h_controller.index()


def teste(request):
	"""pagina de teste da visualizacao hiperbolica"""
	h_controller = HiperbolicaController(request)
	return h_controller.teste()
	
def mostrar_arvore(request):
	"""carrega e mostra a arvore"""
	
	h_controller = HiperbolicaController(request)
	return h_controller.mostrar_arvore()
