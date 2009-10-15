# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

#from puc.sme2.core.commands import listar_projeto
#from puc.sme2.core.commands.command import commandMap 

'''
def controller(request, *args, **kwargs):
	cmd = request.GET.get('command', None)
	c = commandMap()
	print cmd
	#command = commands.commandMap[cmd]
	command = listar_projeto.listarProjetosCommand()
	print 'command name: %s' % command.name
	print 'command template: %s'  % command.template
	return command.execute(request, *args, **kwargs)
'''

def listar_projeto(request):
	return HttpResponse("<h1>listar projeto</h1>")

def listar_alarme(request):
	return HttpResponse("<h1>listar alarme</h1>")
	
def listar_monitor(request):
	return HttpResponse("<h1>listar monitor</h1>")