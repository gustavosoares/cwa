from time import gmtime, strftime

#Classe que representa o evento
class Evento():
	def __init__(self, monitor, row):
		self.monitor = monitor
		self.row = row
		self.tipo = row[0]
		self.data_hora = row[1]
		self.servidor = row[2]
		self.data = row[3:]
		
	#retorna string formatada
	def get_data_hora_formatada(self):
		return self.data_hora.strftime('%d/%m/%Y %H:%M:%S')
		
	def __str__(self):
		return u'Evento do monitor id %s' % self.monitor.mon_id

		