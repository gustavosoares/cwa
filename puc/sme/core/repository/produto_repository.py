
from django.conf import settings
from puc.sme.models import Produto
from puc.sme.core.repository import alarme_repository

def get_produtos():
	"""retorna todos os produtos"""
	return Produto.objects.all()
	
def get_produtos_alarmando():
	"""retorna todos os produtos em alarme ou warning"""
	return Produto.objects.exclude(prd_status='X')

def get_produto_por_id(id):
	"""retorna o produto pelo id passado"""
	return Produto.objects.get(prd_id=id)
	
def get_produtos_e_seus_alarmes():
	"""etorna produtos alarmando e seus alarmes"""
	produtos_alarmes = []
	produtos = get_produtos_alarmando()
	for produto in produtos:
		alarmes = alarme_repository.get_alarmes_por_produto_id(produto.prd_id)
		produtos_alarmes.append({'produto' : produto, 'alarmes' : alarmes})
	return produtos_alarmes

def limpa_produto_por_id(id):
	"""marca o produto com prd_status = X"""
	Produto.objects.filter(prd_id=id).update(prd_status='X')