from time import gmtime, strftime

class Evento():
	"""Classe que representa um evento no sme"""
	def __init__(self, monitor, alarme, metadados):
		self.id = metadados[1]['id']
		self.monitor = monitor
		self.alarme = alarme
		self.descricao_colunas = [] #array com a descriacao das colunas
		for ordem, var in metadados.items():
			self.descricao_colunas.append(var['descricao'])
			
		#self.id = row[0] #coluna pad_id no banco de dados
		self.tipo = metadados[1]['severidade'] #tipo do evento: alarme ou warning
		self.data_hora = metadados[1]['valor']
		self.servidor = metadados[2]['valor']
		del metadados[1]
		del metadados[2]
		self.metadados = metadados
		'''
		Exemplo de metadado:
		{1L: {'ordem': 1L, 'nome': u'pad_datahora', 'tipo': u'D', 'descricao': u'Data / Hora', 'valor': datetime.datetime(2009, 9, 20, 21, 50, 1)}, 
		2L: {'ordem': 2L, 'nome': u'pad_nomemaquina', 'tipo': u'T', 'descricao': u'Servidor', 'valor': u'riosb74'}, 
		3L: {'ordem': 3L, 'nome': u'log', 'tipo': u'T', 'descricao': u'log', 'valor': u'bbb9.log'}, 
		4L: {'ordem': 4L, 'nome': u'erro', 'tipo': u'N', 'descricao': u'numeros de erros', 'valor': Decimal("39.000")}, 
		5L: {'ordem': 5L, 'nome': u'exception', 'tipo': u'T', 'descricao': u'exception', 'valor': u'BEA-101020 '}}
		'''


	def get_data_hora_formatada(self):
		"""retorna data e hora formata em string"""
		return self.data_hora.strftime('%d/%m/%Y %H:%M:%S')
	
#	def get_dados(self):
#		return self.dados
		
	def __str__(self):
		return u'Evento do monitor id %s' % self.monitor.mon_id
