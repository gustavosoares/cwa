
from django.conf import settings
from puc.sme.models import Alarme

#retorna todos os alarmes de um determinado produto
def get_alarmes_por_produto_id(id):
	return Alarme.objects.exclude(alm_status='X').filter(prd_id=id)
	
		
