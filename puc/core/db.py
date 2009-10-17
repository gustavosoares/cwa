import MySQLdb
from django.db import connection

#wrapper de acesso ao banco de dados
class Database():
	def __init__(self):
		self.cursor = connection.cursor()
		self.rows = None
		self.rows_afetadas = 0
	
	#executes a sql
	def execute(self, sql):
		print 'Database sql:\n%s' % sql
		self.rows_afetadas = self.cursor.execute(sql)
	
	#get rows
	def rows_fetchall(self):
		self.rows = self.cursor.fetchall()
		return self.rows
		
	def rows_count(self):
		return len(rows)
		
