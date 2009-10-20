# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.core.db import Database
from puc.sme.models import Monitor


class MonitorRepository(Singleton):
	def get_monitores(self):
		"""retorna todos os monitores"""
		return Monitor.objects.all()

	def get_monitor_alarmando_por_alarme_id(self,id):
		"""busca um monitor alarmando por alarme id"""
		return Monitor.objects.exclude(mon_status='X').filter(alm_id=id)

	def get_monitor_por_alarme_id(self,id):
		"""busca um monitores por alarme id"""
		return Monitor.objects.filter(alm_id=id)

	def get_monitor_por_id(self,id):
		"""busca um monitor por id"""
		return Monitor.objects.get(mon_id=id)

	def limpa_monitor_por_id(self,id):
		"""marca o monitor com nenhum alarme"""
		Monitor.objects.filter(mon_id=id).update(mon_status='X')

	def get_colunas_por_monitor_id(self,id):
		"""retorna duas lista de colunas (desc e nome) de um monitor id"""
		sql = """
		select mon_id, col_cabecalho, col_nomefisico, col_tipo, col_ordem
		from coluna 
		where mon_id = %s
		ORDER BY col_ordem
		""" % id
		db = Database()
		db.execute(sql)
		rows = db.rows_fetchall()
		colunas_desc = []
		colunas_nome = []
		for coluna in rows:
			colunas_desc.append(coluna[1])
			colunas_nome.append(coluna[2])

		return colunas_desc, colunas_nome

	def get_eventos_por_monitor_id(self,id):
		"""obtem lista eventos por monitor id"""
		monitor = self.get_monitor_por_id(id)
		#colunas_desc: descricao do nome da coluna
		#colunas_nome: nome fisico da coluna no banco de dados
		colunas_desc, colunas_nome = self.get_colunas_por_monitor_id(id)

		#monto a string para ser usado no select
		aux = ''
		aux_size = len(colunas_nome)
		count = 1
		for coluna in colunas_nome:
			if (count == aux_size):
				aux = aux + coluna
			else:
				aux = aux + coluna + ', '
			count = count + 1

		sql = """
		select pad_id, pad_tipoalarme, %s
		from %s
		where mon_id = %s
		AND pad_verificado  = 'N'
		AND pad_tipoalarme <> 'X'
		ORDER BY pad_datahora DESC LIMIT 2000
		""" % (aux, monitor.mon_tabela, monitor.mon_id)
		db = Database()
		db.execute(sql)
		rows = db.rows_fetchall()
		return rows, monitor, colunas_desc, colunas_nome
		
	def get_eventos_por_periodo_por_monitor_id(self,id,data_inicio_str,data_fim_str):
		"""obtem lista eventos em um periodo por monitor id"""
		monitor = self.get_monitor_por_id(id)
		#colunas_desc: descricao do nome da coluna
		#colunas_nome: nome fisico da coluna no banco de dados
		colunas_desc, colunas_nome = self.get_colunas_por_monitor_id(id)

		#monto a string com os nomes das colunas para ser usado no select
		aux = ''
		aux_size = len(colunas_nome)
		count = 1
		for coluna in colunas_nome:
			if (count == aux_size):
				aux = aux + coluna
			else:
				aux = aux + coluna + ', '
			count = count + 1

		sql = """
		select pad_id, pad_tipoalarme, %s
		from %s
		where mon_id = %s
		AND pad_datahora  >= '%s 00:00:00'
		AND pad_datahora <= '%s 23:59:59'
		ORDER BY pad_datahora DESC LIMIT 2000
		""" % (aux, monitor.mon_tabela, monitor.mon_id, data_inicio_str, data_fim_str)
		db = Database()
		db.execute(sql)
		rows = db.rows_fetchall()
		return rows, monitor, colunas_desc, colunas_nome		

	def fechar_evento(self, id, monitor, alarme, produto):
		"""fecha um evento"""
		sql = """
		UPDATE %s
		SET pad_verificado = 'S', pad_datahoraverificado = SYSDATE()
		WHERE pad_id = %s
		""" % (monitor.mon_tabela, id)
		db = None

		db = Database()
		db.execute(sql)
		db.close_connection()
		#algum mon_id alarmando na tabela do monitor?
		sql = """
		SELECT pad_id FROM %s
		WHERE mon_id = %s AND pad_tipoalarme <> 'X' AND pad_verificado = 'N' LIMIT 1
		""" % (monitor.mon_tabela, monitor.mon_id)
		db.execute(sql)
		db.rows_fetchall()
		#Imports necessarios das classes
		from puc.sme.core.repository.alarme_repository import AlarmeRepository
		from puc.sme.core.repository.produto_repository import ProdutoRepository
		if (db.rows_count() == 0):
			#atualizo mon_status na tabela do monitor
			print '###limpando monitor...'
			self.limpa_monitor_por_id(monitor.mon_id)

		#algum alm_id alarmando na tabela monitor?
		if (len(self.get_monitor_alarmando_por_alarme_id(alarme.alm_id)) == 0):
			print '###limpando alarme...'
			#atualizo alm_status na tabela do monitor
			AlarmeRepository().limpa_alarme_por_id(alarme.alm_id)

		#algum prd_id alarmando na tabela alarme?
		if (len(AlarmeRepository().get_alarmes_alarmando_por_produto_id(produto.prd_id)) == 0):
			print '###limpando produto...'
			ProdutoRepository().limpa_produto_por_id(produto.prd_id)

	def fechar_todos_eventos(self, monitor, alarme, produto):
		"""docstring for fechar_todos_eventos"""
		pass


