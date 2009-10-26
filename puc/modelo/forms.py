from django.db import models
from django import forms
from puc.modelo.models import Modelo

class MyModeloAdminForm(forms.ModelForm):
	metadado = forms.CharField(widget=forms.HiddenInput, label=u'', max_length=800)

	#metadado = models.CharField(max_length=800, null=True, blank=True, help_text="metadado com a ordem das visoes")
	
	class Meta:
		model = Modelo
