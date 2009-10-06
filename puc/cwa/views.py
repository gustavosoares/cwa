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
	return HttpResponse('<h1>index</h1>')

	
def widget(request):
	return render_to_response('teste.html')

def chart(request):
	return render_to_response('sample.html')