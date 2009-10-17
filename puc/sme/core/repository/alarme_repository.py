
from django.conf import settings
from puc.sme.models import Alarme

def get_alarmes_por_produto_id(id):
	"""retorna todos os alarmes de um determinado produto"""
	return Alarme.objects.exclude(alm_status='X').filter(prd_id=id)

def get_alarme_por_id(id):
	"""retorna alarme por id"""
	return Alarme.objects.get(alm_id=id)

def limpa_alarme_por_id(id):
	"""marca o alarme com alm_status = X"""
	Alarme.objects.filter(alm_id=id).update(alm_status='X')