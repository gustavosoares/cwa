# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	  * Rearrange models' order
#	  * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class Alarme(models.Model):
	alm_nome = models.CharField(max_length=150)
	prd_id = models.IntegerField(null=True, blank=True)
	alm_status = models.CharField(max_length=3)
	alm_id = models.IntegerField(primary_key=True)
	alm_alarmar = models.CharField(max_length=3)
	class Meta:
		db_table = u'alarme'
		ordering = ['alm_nome']

	def __unicode__(self):
		return self.alm_nome
		
	def get_monitores_alarmando(self):
		from puc.sme.core.repository.monitor_repository import MonitorRepository
		return MonitorRepository().get_monitor_alarmando_por_alarme_id(self.alm_id)

class Alarmehelp(models.Model):
	mem_id = models.IntegerField(primary_key=True)
	alm_id = models.IntegerField()
	alm_body = models.CharField(max_length=765)
	class Meta:
		db_table = u'alarmehelp'

class Alarmehistorico(models.Model):
	alm_id = models.IntegerField()
	alh_datahora = models.DateTimeField(null=True, blank=True)
	alh_datahoravisto = models.DateTimeField(null=True, blank=True)
	alh_emailenviado = models.CharField(max_length=3)
	alh_id = models.IntegerField(primary_key=True)
	mon_id = models.IntegerField(null=True, blank=True)
	pad_id = models.IntegerField(null=True, blank=True)
	alh_tipoalarme = models.CharField(max_length=3)
	class Meta:
		db_table = u'alarmehistorico'

class Coluna(models.Model):
	col_cabecalho = models.CharField(max_length=150)
	col_nomefisico = models.CharField(max_length=150, blank=True)
	col_tipo = models.CharField(max_length=3, blank=True)
	col_ordem = models.IntegerField()
	mon_id = models.IntegerField(null=True, blank=True)
	col_exibir = models.CharField(max_length=3, blank=True)
	col_id = models.IntegerField(primary_key=True)
	col_valoralarme = models.CharField(max_length=150, blank=True)
	col_valorwarning = models.CharField(max_length=150, blank=True)
	col_tamanho = models.IntegerField(null=True, blank=True)
	col_ativaemail = models.CharField(max_length=3)
	class Meta:
		db_table = u'coluna'

class Produto(models.Model):
	prd_nome = models.CharField(max_length=150)
	prd_sigla = models.CharField(max_length=9)
	prd_status = models.CharField(max_length=3)
	prd_id = models.IntegerField(primary_key=True)
	prd_alarmar = models.CharField(max_length=3)
	class Meta:
		db_table = u'produto'
		ordering = ['prd_nome']

	def __unicode__(self):
		return self.prd_nome

class Produtohelp(models.Model):
	mem_id = models.IntegerField(primary_key=True)
	prd_id = models.IntegerField()
	prd_body = models.CharField(max_length=765)
	class Meta:
		db_table = u'produtohelp'
		
class Monitor(models.Model):
	mon_nome = models.CharField(max_length=150, blank=True)
	mon_xml = models.CharField(max_length=9)
	alm_id = models.IntegerField(null=True, blank=True)
	mon_status = models.CharField(max_length=3)
	mon_tabela = models.CharField(max_length=150)
	mon_id = models.IntegerField(primary_key=True)
	mon_timeout = models.IntegerField(null=True, blank=True)
	mon_ultima = models.DateTimeField(null=True, blank=True)
	mon_execucao = models.CharField(max_length=3, blank=True)
	mon_alarmar = models.CharField(max_length=3)
	mon_ultimoaviso = models.DateTimeField(null=True, blank=True)
	mon_validade = models.IntegerField(null=True, blank=True)
	mon_tipolimpeza = models.CharField(max_length=3, blank=True)
	mon_pathlimpa = models.CharField(max_length=765, blank=True)
	mon_disponibilidade = models.CharField(max_length=3)
	mon_faq = models.CharField(max_length=765, blank=True)
	class Meta:
		db_table = u'monitor'
		ordering = ['mon_nome']

	def __unicode__(self):
		return '%s - %s' % (self.mon_id, self.mon_nome)

class Monitoremail(models.Model):
	mem_id = models.IntegerField(primary_key=True)
	mon_id = models.IntegerField(null=True, blank=True)
	mon_emailbody = models.CharField(max_length=765)
	class Meta:
		db_table = u'monitoremail'

class Monitorhelp(models.Model):
	mem_id = models.IntegerField(primary_key=True)
	mon_id = models.IntegerField(null=True, blank=True)
	mon_body = models.CharField(max_length=765)
	class Meta:
		db_table = u'monitorhelp'