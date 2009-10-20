# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.sme.models import Alarme
from puc.sme.core.repository.monitor_repository import *

class AlarmeRepository(Singleton):
	@staticmethod
	def get_alarmes():
		"""retorna todos os alarmes"""
		return Alarme.objects.all()
	
	@staticmethod
	def get_alarmes_alarmando_por_produto_id(id):
		"""retorna todos os alarmes alarmando de um determinado produto"""
		return Alarme.objects.exclude(alm_status='X').filter(prd_id=id)

	@staticmethod
	def get_alarmes_por_produto_id(id):
		"""retorna todos os alarmes de um determinado produto"""
		return Alarme.objects.filter(prd_id=id)

	@staticmethod
	def get_alarme_por_id(id):
		"""retorna alarme por id"""
		return Alarme.objects.get(alm_id=id)

	@staticmethod
	def limpa_alarme_por_id(id):
		"""marca o alarme com alm_status = X"""
		Alarme.objects.filter(alm_id=id).update(alm_status='X')

	@staticmethod
	def get_alarme_monitor_xref():
		alarmes = AlarmeRepository.get_alarmes()
		monitores = MonitorRepository.get_monitores()
		alarmes_monitores = {}
		for monitor in monitores:
			l = alarmes_monitores.get(monitor.alm_id,[])
			l.append({'mon_nome' : monitor.mon_nome, 'mon_id' : monitor.mon_id})
			alarmes_monitores[monitor.alm_id] = l
			
		return alarmes_monitores
