import MySQLdb
from puc.sme2.core import util
from django.db import connection

#wrapper de acesso ao banco de dados
class Database():
	def __init__(self):
		self.cursor = self.get_connection()
		self.rows = None
		self.rows_afetadas = 0
	
	def get_connection(self):
		"""opens a connection"""
		return connection.cursor()
		
	def close_connection(self):
		"""fecha o cursor"""
		self.cursor.close()
		self.cursor = None
	   
	#executes a sql
	def execute(self, sql):
		"""executes a sql"""
		inicio = util.start_counter()
		#print 'Database sql:\n%s' % sql
		if not self.cursor:
			self.cursor = self.get_connection()
		self.rows_afetadas = self.cursor.execute(sql)
		
		elapsed = util.elapsed(inicio)
	
	#get rows
	def rows_fetchall(self):
		"""pegat todas as linhas"""
		self.rows = self.cursor.fetchall()
		return self.rows
		
	def rows_count(self):
		"""conta as linhas"""
		if self.rows:
			return len(self.rows)
		else:
			return 0
	
