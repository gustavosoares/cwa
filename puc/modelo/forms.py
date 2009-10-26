from django.db import models
from django import forms
from puc.modelo.models import Modelo

class MyModeloAdminForm(forms.ModelForm):
	metadado = forms.CharField(widget=forms.HiddenInput, label=u'Metadado', max_length=800)
	#metadado = forms.CharField(label=u'Metadado', max_length=800)
	
	class Meta:
		model = Modelo
