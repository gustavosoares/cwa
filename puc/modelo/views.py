# coding=utf-8
# coding=utf-8
from puc.modelo.controller import ModeloController

def ver_template(request, template_id=None):
	#return listar_produto_alarme(request)
	modelo_controller = ModeloController(request)
	return modelo_controller.ver_template(template_id)
