#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Modelo(models.Model):
	nome = models.CharField(max_length=100)
	descricao = models.CharField(max_length=500, blank=True, null=True)
	metadado = models.CharField(max_length=800,)
	estado = models.BooleanField(verbose_name='Ativo?')
	
	def __unicode__(self):
		return u'%s' % self.nome
		
	class Meta:
		ordering = ['nome']

class VisaoRelatorio(models.Model):
	
	RELATORIO_CHOICES = (
		('tabular', 'Relatório tabular'),
		('grafico-linha', 'Relatório com gráfico de linha'),
		('grafico-barra', 'Relatório com gráfico de barras'),
	)
	
	formato = models.CharField(max_length=500, blank=True, null=True, choices=RELATORIO_CHOICES)

	def __unicode__(self):
		return u'%s' % self.formato

	class Meta:
		ordering = ['formato']

		
	
