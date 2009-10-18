
from django.conf import settings
from puc.core.singleton import Singleton
from puc.sme.models import Produto
from puc.sme.core.repository.alarme_repository import AlarmeRepository

class ProdutoRepository(Singleton):
	@staticmethod
	def get_produtos():
		"""retorna todos os produtos"""
		return Produto.objects.all()

	@staticmethod
	def get_produtos_alarmando():
		"""retorna todos os produtos em alarme ou warning"""
		return Produto.objects.exclude(prd_status='X')

	@staticmethod
	def get_produto_por_id(id):
		"""retorna o produto pelo id passado"""
		return Produto.objects.get(prd_id=id)

	@staticmethod	
	def get_produtos_e_seus_alarmes():
		"""etorna produtos alarmando e seus alarmes"""
		produtos_alarmes = []
		produtos = ProdutoRepository.get_produtos_alarmando()
		for produto in produtos:
			alarmes = AlarmeRepository.get_alarmes_por_produto_id(produto.prd_id)
			produtos_alarmes.append({'produto' : produto, 'alarmes' : alarmes})
		return produtos_alarmes

	@staticmethod
	def limpa_produto_por_id(id):
		"""marca o produto com prd_status = X"""
		Produto.objects.filter(prd_id=id).update(prd_status='X')