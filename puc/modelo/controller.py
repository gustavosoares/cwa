# coding=utf-8
from puc.core.controller import Controller

from traceback import *
import sys
import copy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from puc import templates
from puc.core import json
from puc.modelo.models import Modelo, VisaoRelatorio, VisaoHierarquica, Widget, TemplateModelo
from puc.modelo.repository import ModeloRepository, WidgetRepository, TemplateModeloRepository

modelo_repository = ModeloRepository()
template_repository = TemplateModeloRepository()


class ModeloController(Controller):
	
	def ver_template(template_id):
		return HttpResponse("ver template");