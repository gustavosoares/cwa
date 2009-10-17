from time import gmtime, strftime

#Classe que representa o evento
class Evento():
	def __init__(self, monitor, alarme, row):
		self.monitor = monitor
		self.alarme = alarme
		self.row = row
		self.id = row[0] #coluna pad_id no banco de dados
		self.tipo = row[1] #tipo do evento: alarme ou warning
		self.data_hora = row[2]
		self.servidor = row[3]
		self.dados = row[4:]
		
		
	#retorna string formatada
	def get_data_hora_formatada(self):
		return self.data_hora.strftime('%d/%m/%Y %H:%M:%S')
	
	def get_dados(self):
		return self.dados	
		
	def __str__(self):
		return u'Evento do monitor id %s' % self.monitor.mon_id

		