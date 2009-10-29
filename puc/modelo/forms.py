# coding=utf-8
from django.db import models
from django import forms
from puc.modelo.models import Modelo, VisaoRelatorio

class MyModeloAdminForm(forms.ModelForm):
	metadado = forms.CharField(widget=forms.TextInput(attrs={'size' : '100', 'readonly' : 'true'}), 
	label=u'Metadado', max_length=800, help_text="Posição das visoes na página. Campo somente leitura")
	
	class Meta:
		model = Modelo
