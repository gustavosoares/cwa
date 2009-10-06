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
	return HttpResponse('teste')