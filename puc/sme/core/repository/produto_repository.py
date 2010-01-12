# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.sme.models import Produto
from puc.sme.core.repository.alarme_repository import AlarmeRepository

class ProdutoRepository(Singleton):
	def get_produtos(self):
		"""retorna todos os produtos"""
		return Produto.objects.all()

	def get_produtos_alarmando(self):
		"""retorna todos os produtos em alarme ou warning"""
		return Produto.objects.exclude(prd_status='X')

	def get_produto_por_id(self, id):
		"""retorna o produto pelo id passado"""
		return Produto.objects.get(prd_id=id)

	def get_produtos_e_seus_alarmes(self):
		"""retorna produtos alarmando e seus alarmes"""
		produtos_alarmes = []
		produtos = self.get_produtos_alarmando()
		for produto in produtos:
			alarmes = AlarmeRepository().get_alarmes_alarmando_por_produto_id(produto.prd_id)
			produtos_alarmes.append({'produto' : produto, 'alarmes' : alarmes})
		return produtos_alarmes

	def limpa_produto_por_id(self,id):
		"""marca o produto com prd_status = X"""
		Produto.objects.filter(prd_id=id).update(prd_status='X')

	def liga_produto_por_id(self, id, tipo_alarme):
		"""liga o produto"""
		Produto.objects.filter(prd_id=id).update(prd_status=tipo_alarme)

	def get_produto_alarme_xref(self):
		produtos = self.get_produtos()
		alarmes = AlarmeRepository().get_alarmes()
		produtos_alarmes = {}
		for alarme in alarmes:
			l = produtos_alarmes.get(alarme.prd_id,[])
			l.append({'alm_nome' : alarme.alm_nome, 'alm_id' : alarme.alm_id})
			produtos_alarmes[alarme.prd_id] = l

		return produtos_alarmes
