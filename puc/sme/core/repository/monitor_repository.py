#-*- coding:utf-8 -*-
import copy
from puc.core.singleton import Singleton
from django.conf import settings
from puc.core.db import Database
from puc.sme.models import Monitor
from puc.sme.core import domain
from puc.sme2.core import util
from django.core.cache import cache

CACHE_TIMEOUT = 86400 * 15 #48horas

class MonitorRepository(Singleton):
	def get_monitores(self):
		"""retorna todos os monitores"""
		return Monitor.objects.all()

	def get_monitores_alarmando_por_alarme_id(self,id):
		"""busca um monitor alarmando por alarme id"""
		return Monitor.objects.exclude(mon_status='X').filter(alm_id=id)

	def get_monitores_por_alarme_id(self,id):
		"""busca um monitores por alarme id"""
		return Monitor.objects.filter(alm_id=id)

	def get_monitor_por_id(self,id):
		"""busca um monitor por id"""
		return Monitor.objects.get(mon_id=id)

	def limpa_monitor_por_id(self,id):
		"""marca o monitor com nenhum alarme"""
		Monitor.objects.filter(mon_id=id).update(mon_status='X')
		
	def liga_monitor_por_id(self, id, tipo_alarme):
		"""marca o monitor com alarme"""
		Monitor.objects.filter(mon_id=id).update(mon_status=tipo_alarme)

	def get_colunas_por_monitor_id(self,id):
		"""
		retorna dicionario com os metadados das colunas para o monitor id
		Ex.: {u'rad_resposta': {'ordem': 3L, 'tipo': u'T', 'descricao': u'Timeout'}, 
		u'pad_datahora': {'ordem': 1L, 'tipo': u'D', 'descricao': u'Data / Hora'}, 
		u'rad_total': {'ordem': 4L, 'tipo': u'N', 'descricao': u'Total'}, 
		u'pad_erro': {'ordem': 5L, 'tipo': u'T', 'descricao': u'Erro'}, 
		u'pad_nomemaquina': {'ordem': 2L, 'tipo': u'T', 'descricao': u'Servidor'}}
		"""
		sql = """
		select mon_id, col_cabecalho, col_nomefisico, col_tipo, col_ordem
		from coluna 
		where mon_id = %s
		ORDER BY col_ordem
		""" % id
		db = Database()
		db.execute(sql)
		rows = db.rows_fetchall()
		colunas = {}
		#colunas_desc = []
		#colunas_nome = []
		for coluna in rows:
			descricao = coluna[1]
			nome = coluna[2]
			if nome == 'pad_datahora':
				nome = 'pad_datahoraalarme'
			tipo = coluna[3]
			ordem = coluna[4]
			#colunas_desc.append(descricao)
			#colunas_nome.append(nome)
			colunas[nome] = {'descricao' : descricao, 'tipo': tipo, 'ordem' : ordem}

		return colunas

	def total_eventos_por_monitor_id(self, id):
		"""retorna o total de eventos por monitor sem gerar o objeto evento"""
		
		inicio = util.start_counter()
		monitor = self.get_monitor_por_id(id)
		from puc.sme.core.repository.alarme_repository import AlarmeRepository
		alarme = AlarmeRepository().get_alarme_por_id(monitor.alm_id)
		#colunas_desc: descricao do nome da coluna
		#colunas_nome: nome fisico da coluna no banco de dados
		#colunas_desc, colunas_nome = self.get_colunas_por_monitor_id(id)
		colunas = self.get_colunas_por_monitor_id(id)
		#print '[MonRepository] colunas: %s' % colunas
		colunas_nome = []
		for nome,metadado in colunas.items():
			colunas_nome.append(nome)
		#monto a string para ser usado no select
		aux = ''
		aux_size = len(colunas_nome)
		count = 1
		clausula_select = [] #array com as colunas do campo do select
		for coluna in colunas_nome:
			clausula_select.append(coluna)
			if (count == aux_size):
				aux = aux + coluna
			else:
				aux = aux + coluna + ', '
			count = count + 1
		
		#alterado em 28/10/2009
		#de pad_datahora para pad_datahoraalarme
		sql = ""

		sql = """
		select pad_id, pad_tipoalarme, %s
		from %s
		where mon_id = %s
		AND pad_verificado	= 'S'
		AND pad_tipoalarme <> 'X'
		ORDER BY pad_datahoraalarme
		""" % (aux, monitor.mon_tabela, monitor.mon_id)

		db = Database()
		db.execute(sql)
		rows = db.rows_fetchall()
		util.elapsed(inicio,'get total de eventos')
		return db.rows_count()
	
	def get_eventos_paginados_por_monitor(self, monitor, pagina_inicio, items_por_pagina):
		"""retorna os eventos paginados"""
		eventos = self.get_eventos_por_monitor_id(monitor.mon_id, inicio=pagina_inicio, limite=items_por_pagina)
		return eventos
		
	def get_eventos_por_monitor_id(self,id,data_inicio_str=None,data_fim_str=None,todos=None,todos_ligados=None,inicio=None,limite=None):
		"""obtem lista eventos por monitor id"""
		monitor = self.get_monitor_por_id(id)
		from puc.sme.core.repository.alarme_repository import AlarmeRepository
		alarme = AlarmeRepository().get_alarme_por_id(monitor.alm_id)
		#colunas_desc: descricao do nome da coluna
		#colunas_nome: nome fisico da coluna no banco de dados
		#colunas_desc, colunas_nome = self.get_colunas_por_monitor_id(id)
		colunas = self.get_colunas_por_monitor_id(id)
		#print '[MonRepository] colunas: %s' % colunas
		colunas_nome = []
		for nome,metadado in colunas.items():
			colunas_nome.append(nome)
		#monto a string para ser usado no select
		aux = ''
		aux_size = len(colunas_nome)
		count = 1
		clausula_select = [] #array com as colunas do campo do select
		for coluna in colunas_nome:
			clausula_select.append(coluna)
			if (count == aux_size):
				aux = aux + coluna
			else:
				aux = aux + coluna + ', '
			count = count + 1
		
		#alterado em 28/10/2009
		#de pad_datahora para pad_datahoraalarme
		sql = ""
		if data_inicio_str and data_fim_str and not todos:
			sql = """
			select pad_id, pad_tipoalarme, %s
			from %s
			where mon_id = %s
			AND pad_datahoraalarme	>= '%s 00:00:00'
			AND pad_datahoraalarme <= '%s 23:59:59'
			ORDER BY pad_datahora DESC LIMIT 2000
			""" % (aux, monitor.mon_tabela, monitor.mon_id, data_inicio_str, data_fim_str)
		elif todos:
			sql = """
			select pad_id, pad_tipoalarme, %s
			from %s
			where mon_id = %s
			AND pad_verificado	= 'N'
			AND pad_tipoalarme <> 'X'
			ORDER BY pad_datahoraalarme
			""" % (aux, monitor.mon_tabela, monitor.mon_id)
		elif todos_ligados:
			sql = """
			select pad_id, pad_tipoalarme, %s
			from %s
			where mon_id = %s
			AND pad_verificado	= 'S'
			AND pad_tipoalarme <> 'X'
			ORDER BY pad_datahoraalarme
			""" % (aux, monitor.mon_tabela, monitor.mon_id)
		elif inicio != None and limite != None:
			sql = """
			select pad_id, pad_tipoalarme, %s
			from %s
			where mon_id = %s
			AND pad_verificado	= 'S'
			AND pad_tipoalarme <> 'X'
			ORDER BY pad_datahoraalarme LIMIT %s,%s
			""" % (aux, monitor.mon_tabela, monitor.mon_id, inicio, limite)
		else:
			sql = """
			select pad_id, pad_tipoalarme, %s
			from %s
			where mon_id = %s
			AND pad_verificado	= 'N'
			AND pad_tipoalarme <> 'X'
			ORDER BY pad_datahoraalarme DESC LIMIT 5000
			""" % (aux, monitor.mon_tabela, monitor.mon_id)
		db = Database()
		db.execute(sql)
		inicio = util.start_counter()
		rows = db.rows_fetchall()
		util.elapsed(inicio,'fetch all events')
		
		inicio = util.start_counter()
		eventos = []
		"""
		O dicionario controla_duplicados armazena o nome do host e a hora do evento.
		Ela é usada para evitar que se tenha dado duplicado no relatorio,
		garantido que sempre esteja o maior valor.
		"""
		controla_duplicados = {}
		#finalizo a construcao do metadado do evento
		tempo_objeto = 0.0
		for row in rows:
			new_row = row[2:]
			i = 0
			metadados = {}
			for coluna_nome in clausula_select:
				var = colunas[coluna_nome]
				ordem = var['ordem']
				var['valor'] = new_row[i]
				var['nome'] = coluna_nome
				#severidade do evento: normal, warning, alarme
				var['id'] = row[0]
				var['severidade'] = row[1]
				metadados[ordem] = var
				i = i + 1
			
			inicio2 = util.start_counter()
			
			id_to_check = metadados[1]['id']
			key_cache = 'evento_%s' % id_to_check
			evento_cached = cache.get(key_cache)
			evento_copy = None
			if evento_cached:
				evento_copy = evento_cached
				#print '%s obtido do cache!' % id_to_check
			else:
				evento = domain.Evento(monitor, alarme, metadados)
				evento_copy = copy.deepcopy(evento)
				cache.set(key_cache, evento_copy, CACHE_TIMEOUT)
			
			elapsed2 = util.elapsed(inicio2, 'objeto evento', False)
			tempo_objeto = tempo_objeto + elapsed2
			
			eventos.append(evento_copy)
		
		print '### tempo dos objetos somados: %f' % tempo_objeto
		util.elapsed(inicio,'construção lista eventos')
		return eventos
		
	def get_eventos_por_periodo_por_monitor_id(self,id,data_inicio_str,data_fim_str):
		"""obtem lista eventos em um periodo por monitor id"""
		return self.get_eventos_por_monitor_id(id,data_inicio_str,data_fim_str)

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
		if (len(self.get_monitores_alarmando_por_alarme_id(alarme.alm_id)) == 0):
			print '###limpando alarme...'
			#atualizo alm_status na tabela do monitor
			AlarmeRepository().limpa_alarme_por_id(alarme.alm_id)

		#algum prd_id alarmando na tabela alarme?
		if (len(AlarmeRepository().get_alarmes_alarmando_por_produto_id(produto.prd_id)) == 0):
			print '###limpando produto...'
			ProdutoRepository().limpa_produto_por_id(produto.prd_id)

	def get_todos_eventos(self, monitor):
		"""retorna os primeitos 30000 eventos"""
		eventos = self.get_eventos_por_monitor_id(monitor.mon_id, todos_ligados=True)
		return eventos
		
	def fechar_todos_eventos(self, monitor, alarme, produto):
		"""docstring for fechar_todos_eventos"""
		#pego os eventos do monitor
		eventos = self.get_eventos_por_monitor_id(monitor.mon_id, todos=True)
		for evento in eventos:
			print 'fechando evento %s' % evento.id
			self.fechar_evento(evento.id, monitor, alarme, produto)

	def ligar_evento(self, id, monitor, alarme, produto):
		"""liga um evento"""
		sql = """
		UPDATE %s
		SET pad_verificado = 'N', pad_datahoraverificado = SYSDATE()
		WHERE pad_id = %s
		""" % (monitor.mon_tabela, id)
		db = None

		db = Database()
		db.execute(sql)
		db.close_connection()
		#algum mon_id alarmando na tabela do monitor?
		sql = """
		SELECT pad_id, pad_tipoalarme FROM %s
		WHERE mon_id = %s AND pad_tipoalarme <> 'X' AND pad_verificado = 'S' LIMIT 2000
		""" % (monitor.mon_tabela, monitor.mon_id)
		db.execute(sql)
		rows = db.rows_fetchall()
		#Imports necessarios das classes
		from puc.sme.core.repository.alarme_repository import AlarmeRepository
		from puc.sme.core.repository.produto_repository import ProdutoRepository
		
		tipo_alarme = 'W'
		
		if (db.rows_count() != 0):
			#atualizo mon_status na tabela do monitor
			print '###ligando monitor...'
			for row in rows:
				if row[1] == 'A':
					tipo_alarme = 'A'
					break
			self.liga_monitor_por_id(monitor.mon_id, tipo_alarme)
		
		rows = None
		
		#algum alm_id alarmando na tabela monitor?
		if (len(self.get_monitores_alarmando_por_alarme_id(alarme.alm_id)) != 0):
			print '###ligando alarme...'
			#atualizo alm_status na tabela do monitor
			AlarmeRepository().liga_alarme_por_id(alarme.alm_id, tipo_alarme)

		#algum prd_id alarmando na tabela alarme?
		if (len(AlarmeRepository().get_alarmes_alarmando_por_produto_id(produto.prd_id)) != 0):
			print '###ligando produto...'
			ProdutoRepository().liga_produto_por_id(produto.prd_id, tipo_alarme)


