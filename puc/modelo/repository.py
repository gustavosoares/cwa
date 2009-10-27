# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.modelo.models import Modelo
from puc.core import json

class ModeloRepository(Singleton):

	def get_modelo_por_nome(self, nome_modelo):
		"""retorna o modelo por nome"""
		return Modelo.objects.get(nome=nome_modelo)
		
	def get_modelo_settings(self, nome_modelo):
		"""retorna um json das configuracoes do modelo"""
		modelo = self.get_modelo_por_nome(nome_modelo)
		assert modelo != None, 'Modelo configurado nao existe no sistema!'
		metadado = modelo.metadado
		modelo_settings = {}
		#Ex.:portal-column-0&portal-column-1:block-tabular&portal-column-bottom:block-relatorio
		colunas = metadado.split('&')
		for coluna in colunas:
			visoes = coluna.split(':')
			if len(visoes) > 1:
				container = visoes[0]
				visoes_aux = visoes[1:]
				print '%s ->> %s' % (container, visoes_aux)
				modelo_settings[container] = visoes_aux

		modelo_settings_json = json.encode_json(modelo_settings)

		return modelo_settings_json