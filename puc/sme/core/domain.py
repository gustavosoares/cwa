from time import gmtime, strftime

class Evento():
	"""Classe que representa um evento no sme"""
	def __init__(self, monitor, alarme, row, colunas_desc):
		self.monitor = monitor
		self.alarme = alarme
		self.descricao_colunas = colunas_desc #array com a descriacao das colunas
		self.row = row
		self.id = row[0] #coluna pad_id no banco de dados
		self.tipo = row[1] #tipo do evento: alarme ou warning
		self.data_hora = row[2]
		self.servidor = row[3]
		self.dados = row[4:]


	def get_data_hora_formatada(self):
		"""retorna data e hora formata em string"""
		return self.data_hora.strftime('%d/%m/%Y %H:%M:%S')
	
	def get_dados(self):
		return self.dados
		
	def __str__(self):
		return u'Evento do monitor id %s' % self.monitor.mon_id

		