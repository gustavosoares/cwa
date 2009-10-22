from puc.core.singleton import Singleton
from puc.relatorio.core import domain

class RelatorioFactory(Singleton):
	
	@staticmethod
	def get_relatorio(formato):
		"""metodo estatico para retornar o relatorio"""
		if formato == 'tabular':
			return domain.RelatorioTabular()
		else:
			return None