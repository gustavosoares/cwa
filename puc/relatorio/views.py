# coding=utf-8
from puc.relatorio.core.controller import RelatorioController

def index(request):
	"""Pagina principal da aplicacao por gerar relatorio"""
	relatorio_controller = RelatorioController(request)
	return relatorio_controller.index()

def info(request):
	"""Pagina de ajuda do relatorio"""
	relatorio_controller = RelatorioController(request)
	return relatorio_controller.info()
		
def get_xml(request):
	"""
	retorna o xml para ser gerado pelo framework em flash de geracao de graficos
	Exemplo de request: http://localhost:10000/relatorio/xml?produto=35&alarme=125&monitor=396&data_inicio=2009-08-01&data_fim=2009-10-28
	"""
	relatorio_controller = RelatorioController(request)
	return relatorio_controller.get_xml()

