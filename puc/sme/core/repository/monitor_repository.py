
from django.conf import settings
from puc.sme.models import Monitor

#retorna todos os monitores de um determinado alarme id
def get_monitor_por_alarme_id(id):
	return Monitor.objects.exclude(mon_status='X').filter(alm_id=id)
	
		
