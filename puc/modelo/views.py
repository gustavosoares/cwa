# coding=utf-8
from puc.modelo.controller import ModeloController

def ver_template(request, template_id=None):
	#return listar_produto_alarme(request)
	modelo_controller = ModeloController(request)
	return modelo_controller.ver_template(template_id)

def ajuda(request):
	#ajuda dos templates
	modelo_controller = ModeloController(request)
	return modelo_controller.ajuda()
		
def ver_template_css(request, template_id=None):
	#return listar_produto_alarme(request)
	modelo_controller = ModeloController(request)
	return modelo_controller.ver_template_css(template_id)