from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from puc.sme2.core.commands.command import command


class listarProjetosCommand(command):
	
	def __init__(self):
		command.__init__(self, 'listar_projeto', 'listar_projeto.html')
	
	def execute(request, *args, **kargs):
		return HttpResponse("<h1>listar projeto</h1>")	