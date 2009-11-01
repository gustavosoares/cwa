# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.core import json
from puc.sme.core.repository.produto_repository import ProdutoRepository
from puc.sme.core.repository.monitor_repository import MonitorRepository
from puc.sme.core.repository.alarme_repository import AlarmeRepository

produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()

class ArvoreHiperbolicaRepository(Singleton):
	
	def get_arvore(self):
		"""
		constroi a arvore hiperbolica com os alarmes e retorna um objeto json
		"""