# coding=utf-8
import datetime
import os

# Cproject.htmlreate your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string


def index(request):
	#return HttpResponse('<h1>index</h1><br\> <center><a href="#" onclick="update_widget("content_widget_0");">Update widget</a></center><br />')
	return HttpResponse('<h1>index</h1><br\> <center><a href="/cwa">reload</a></center><br />')

	
def widget(request):
	return render_to_response('teste_widget.html')

def chart(request):
	return render_to_response('teste_chart.html')

def chart2(request):
	return render_to_response('teste_chart2.html')	

def resize(request):
	return render_to_response('teste_resize.html')