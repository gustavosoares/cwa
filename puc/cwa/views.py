# coding=utf-8
from puc.cwa.core.controller import CwaController

def index(request):
	"""Pagina principal da aplicacao cwa"""
	
	cwa_controller = CwaController(request)
	return cwa_controller.index()
	
def widget(request):
	
	cwa_controller = CwaController(request)
	return cwa_controller.widget()

def chart(request):
	
	cwa_controller = CwaController(request)
	return cwa_controller.chart()

def chart2(request):
	
	cwa_controller = CwaController(request)
	return cwa_controller.chart2()

def resize(request):
	
	cwa_controller = CwaController(request)
	return cwa_controller.resize()
	
def chart_scroll(request):
	
	cwa_controller = CwaController(request)
	return cwa_controller.chart_scroll()
	