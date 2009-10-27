# coding=utf-8
from puc.core.singleton import Singleton
from puc.relatorio.core import domain

class RelatorioFactory(Singleton):
	"""fábrica de criação de relatórios"""
	@staticmethod
	def get_relatorio(formato):
		"""metodo estatico para retornar o relatorio"""
		if formato == 'tabular':
			return domain.RelatorioTabular()
		elif formato == 'grafico-linha':
			return domain.RelatorioGraficoLinha()
		elif formato == 'grafico-barra':
			return domain.RelatorioGraficoBarra()
		else:
			return None
			
class GraficoFactory(Singleton):
	"""fábrica de criação de gráficos"""
	@staticmethod
	def get_grafico(tipo):
		"""metodo estatico para retornar o grafico"""
		if tipo == 'linha':
			return domain.GraficoLinha()
		elif tipo == 'barra':
			return domain.GraficoBarra()
		else:
			return None