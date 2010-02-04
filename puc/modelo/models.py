#-*- coding:utf-8 -*-
from django.db import models

class Widget(models.Model):
	
	nome = models.CharField(max_length=100)
	descricao = models.CharField(max_length=200)
	url = models.CharField(max_length=100)
	url_ajuda = models.CharField(verbose_name='Url de ajuda', max_length=100, blank=True, null=True,)
	width = models.CharField(max_length=4)
	height = models.CharField(max_length=4)
	
	def __unicode__(self):
		return u'%s' % self.nome
		
	class Meta:
		ordering = ['nome']
		
class TemplateModelo(models.Model):
	
	nome = models.CharField(max_length=100)
	nome_arquivo_css = models.CharField(verbose_name='Nome do arquivo css', max_length=100)
	nome_arquivo_html = models.CharField(verbose_name='Nome do arquivo html', max_length=100)
	
	def __unicode__(self):
		return u'%s' % self.nome
		
	class Meta:
		ordering = ['nome']
		verbose_name_plural = u'Templates'
		verbose_name = u'Template'
		
# Create your models here.
class Modelo(models.Model):
	nome = models.CharField(max_length=100, help_text="Nome do modelo/painel criado.")
	descricao = models.CharField(max_length=500, blank=True, null=True,help_text="Sucinta explicação do modelo. Campo opcional.")
	metadado = models.CharField(max_length=800,)
	template = models.ForeignKey(TemplateModelo)
	estado = models.BooleanField(verbose_name='Ativo?',help_text='Habilta/Desabilita o modelo.')
	
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
		verbose_name_plural = u'Configurar Visão Relatório'

class VisaoHierarquica(models.Model):

	frequencia_atualizacao = models.PositiveIntegerField(verbose_name='Frequência de atualização (seg)', blank=False, null=False)

	def __unicode__(self):
		return u'%s' % self.frequencia_atualizacao

	class Meta:
		ordering = ['frequencia_atualizacao']
		verbose_name_plural = u'Configurar Visão Hierárquica'
