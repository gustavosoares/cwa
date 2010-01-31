# coding=utf-8
from django.db import models
from django import forms
from puc.modelo.models import Modelo, VisaoRelatorio, TemplateModelo

class MyModeloAdminForm(forms.ModelForm):
	metadado = forms.CharField(widget=forms.TextInput(attrs={'size' : '100', 'readonly' : 'true'}), 
	label=u'Metadado', max_length=800, help_text="Posição das visoes na página. Campo somente leitura")
	
	window_open_str = "<a class=\"block-info\" href='#' onclick=\"window.open('/modelo/template/ajuda/', 'info', 'location=no, tollbars=no, status=no, scrollbars=yes, resizable=yes, menubar=no, height=520, width=630')\"><img height=20 width=20 src=/media/images/question_mark_icon_02_b.gif border=0></a>"
	template = forms.ModelChoiceField(queryset=TemplateModelo.objects.all(), label=u'Template', 
	help_text='O que é isso? '+window_open_str)
	
	class Meta:
		model = Modelo
