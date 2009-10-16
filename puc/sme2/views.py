# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

#importa modelos
from puc.sme.models import Produto, Alarme, Monitor
from puc.sme.core.repository import produto_repository

#retorna a listagem dos produtos no sme2
def listar_produto(request):
	#template com logica de apresentacao
	template_name = 'listar_produto.html'
	
	booAlarmar = False
	booAlarmarWarning = False
	booAlarmarAlarme = False
	produtos = produto_repository.get_produtos()
	print produtos
	
	return render_to_response(template_name, { 'produtos' : produtos })

def listar_alarme(request):
	return HttpResponse("<h1>listar alarme</h1>")
	
def listar_monitor(request):
	return HttpResponse("<h1>listar monitor</h1>")