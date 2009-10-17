
from django.conf import settings
from puc.sme.models import Produto
from puc.sme.core.repository import alarme_repository

#retorna todos os produtos
def get_produtos():
	return Produto.objects.all()
	
#retorna todos os produtos em alarme ou warning
def get_produtos_alarmando():
	return Produto.objects.exclude(prd_status='X')

#retorna o produto pelo id passado
def get_produto_por_id(id):
	return Produto.objects.get(prd_id=id)
	
#retorna produtos alarmando e seus alarmes
def get_produtos_e_seus_alarmes():
	produtos_alarmes = []
	produtos = get_produtos_alarmando()
	for produto in produtos:
		alarmes = alarme_repository.get_alarmes_por_produto_id(produto.prd_id)
		produtos_alarmes.append({'produto' : produto, 'alarmes' : alarmes})
	return produtos_alarmes
