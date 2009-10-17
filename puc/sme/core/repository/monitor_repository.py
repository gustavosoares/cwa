from django.conf import settings
from puc.core.db import Database
from puc.sme.models import Monitor

#retorna todos os monitores de um determinado alarme id
def get_monitor_por_alarme_id(id):
	return Monitor.objects.exclude(mon_status='X').filter(alm_id=id)

#retorna o monitor por id
def get_monitor_por_id(id):
	return Monitor.objects.get(mon_id=id)

#retorn duas lista de colunas (desc e nome) de um monitor id
def get_colunas_por_monitor_id(id):
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

#obtem lista eventos por monitor id
def get_eventos_por_monitor_id(id):
	monitor = get_monitor_por_id(id)
	colunas_desc, colunas_nome = get_colunas_por_monitor_id(id)
	
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
	select pad_tipoalarme, %s
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