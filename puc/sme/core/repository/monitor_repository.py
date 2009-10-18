from django.conf import settings
from puc.core.db import Database
from puc.sme.models import Monitor
from puc.core.singleton import Singleton
from puc.sme.core.repository.alarme_repository import AlarmeRepository
from puc.sme.core.repository.produto_repository import ProdutoRepository

class MonitorRepository(Singleton):
	@staticmethod
	def get_monitores():
		"""retorna todos os monitores"""
		return Monitor.objects.all()
	
	@staticmethod
	def get_monitor_alarmando_por_alarme_id(id):
		"""busca um monitor alarmando por alarme id"""
		return Monitor.objects.exclude(mon_status='X').filter(alm_id=id)

	@staticmethod
	def get_monitor_por_id(id):
		"""busca um monitor por id"""
		return Monitor.objects.get(mon_id=id)

	@staticmethod
	def limpa_monitor_por_id(id):
		"""marca o monitor com nenhum alarme"""
		Monitor.objects.filter(mon_id=id).update(mon_status='X')

	@staticmethod		
	def get_colunas_por_monitor_id(id):
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

	@staticmethod
	def get_eventos_por_monitor_id(id):
		"""obtem lista eventos por monitor id"""
		monitor = MonitorRepository.get_monitor_por_id(id)
		colunas_desc, colunas_nome = MonitorRepository.get_colunas_por_monitor_id(id)
	
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
		ORDER BY pad_datahora DESC
		""" % (aux, monitor.mon_tabela, monitor.mon_id)
		db = Database()
		db.execute(sql)
		rows = db.rows_fetchall()
		return rows, monitor, colunas_desc, colunas_nome

	@staticmethod
	def fechar_evento(id, monitor, alarme, produto):
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
		if (db.rows_count() == 0):
			#atualizo mon_status na tabela do monitor
			print '###limpando monitor...'
			limpa_monitor_por_id(monitor.mon_id)
	
		#algum alm_id alarmando na tabela monitor?
		if (len(MonitorRepository.get_monitor_alarmando_por_alarme_id(alarme.alm_id)) == 0):
			print '###limpando alarme...'
			#atualizo alm_status na tabela do monitor
			AlarmeRepository.limpa_alarme_por_id(alarme.alm_id)
	
		#algum prd_id alarmando na tabela alarme?
		if (len(AlarmeRepository.get_alarmes_por_produto_id(produto.prd_id)) == 0):
			print '###limpando produto...'
			ProdutoRepository.limpa_produto_por_id(produto.prd_id)

	@staticmethod
	def fechar_todos_eventos(monitor, alarme, produto):
		"""docstring for fechar_todos_eventos"""
		pass
	
	