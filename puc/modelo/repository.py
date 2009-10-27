# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.modelo.models import Modelo

class ModeloRepository(Singleton):
	def get_modelo_por_nome(self, nome_modelo):
		"""retorna o modelo por nome"""
		return Modelo.objects.get(nome=nome_modelo)