# coding=utf-8
import datetime
import os

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from puc import templates


def index(request):
	"""Pagina principal da aplicacao cwa"""
	return HttpResponseRedirect('/admin/')
	#return render_to_response(templates.TEMPLATE_CWA_INDEX)

def criar_modelo(request):
	"""Pagina para criacacao do modelo"""
	return render_to_response(templates.TEMPLATE_CWA_ADMIN_CRIAR_MODELO)
