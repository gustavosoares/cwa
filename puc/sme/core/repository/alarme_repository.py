# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.sme.models import Alarme
from puc.sme.core.repository.monitor_repository import MonitorRepository

class AlarmeRepository(Singleton):
	def get_alarmes(self):
		"""retorna todos os alarmes"""
		return Alarme.objects.all()

	def get_alarmes_alarmando_por_produto_id(self,id):
		"""retorna todos os alarmes alarmando de um determinado produto"""
		return Alarme.objects.exclude(alm_status='X').filter(prd_id=id)

	def get_alarmes_por_produto_id(self,id):
		"""retorna todos os alarmes de um determinado produto"""
		return Alarme.objects.filter(prd_id=id)

	def get_alarme_por_id(self,id):
		"""retorna alarme por id"""
		return Alarme.objects.get(alm_id=id)

	def limpa_alarme_por_id(self,id):
		"""marca o alarme com alm_status = X"""
		Alarme.objects.filter(alm_id=id).update(alm_status='X')

	def liga_alarme_por_id(self, id, tipo_alarme):
		"""liga o alarme"""
		Alarme.objects.filter(alm_id=id).update(alm_status=tipo_alarme)
		
	def get_alarme_monitor_xref(self):
		alarmes = self.get_alarmes()
		monitores = MonitorRepository().get_monitores()
		alarmes_monitores = {}
		for monitor in monitores:
			l = alarmes_monitores.get(monitor.alm_id,[])
			l.append({'mon_nome' : monitor.mon_nome, 'mon_id' : monitor.mon_id})
			alarmes_monitores[monitor.alm_id] = l
		
		return alarmes_monitores
