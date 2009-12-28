# coding=utf-8
from puc.core.singleton import Singleton
from django.conf import settings
from puc.core import json
from puc.sme.core.repository.produto_repository import ProdutoRepository
from puc.sme.core.repository.monitor_repository import MonitorRepository
from puc.sme.core.repository.alarme_repository import AlarmeRepository
from puc.hiperbolica.core import domain
from puc.sme2.core import util
import copy

#Ex.: copy.deepcopy(evento)

produto_repository = ProdutoRepository()
alarme_repository = AlarmeRepository()
monitor_repository = MonitorRepository()

class ArvoreHiperbolicaRepository(Singleton):
	
	def get_arvore(self):
		"""
		constroi a arvore hiperbolica com os alarmes e retorna um objeto json
		"""
		
		eventos_count = {}
		maior = 0
		menor = 1000000
		dim_maximo = 20


		raiz = domain.NoHiperbolico()
		raiz.id = 0
		raiz.name = 'produto'
		raiz.dim = 5
		
		contador = 1
		#pega os produtos alarmando
		produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
		#print 'produtos e alarmes alarmando:\n %s\n' % produtos_alarmes
		
		#pego contagem dos eventos
		for produto_alarmes in produtos_alarmes:
			for alarme in produto_alarmes['alarmes']:
				monitores = monitor_repository.get_monitores_alarmando_por_alarme_id(alarme.alm_id)
				for monitor in monitores:
					eventos = monitor_repository.get_eventos_por_monitor_id(monitor.mon_id)
					c = len(eventos)
					if c > maior:
						maior = c
					if c < menor:
						menor = c
					eventos_count[monitor.mon_id] = c
		
		for produto_alarmes in produtos_alarmes:
			#checo estado do produto
			no_produto = domain.NoHiperbolico()
			no_produto.id = contador
			no_produto.name = produto_alarmes['produto'].prd_nome.encode('utf-8')
			no_produto.dim = 5
			no_produto.type = 'circle'
			if produto_alarmes['produto'].prd_status == 'W':
				no_produto.color = util.colors['warning']
			elif produto_alarmes['produto'].prd_status == 'A':
				no_produto.color = util.colors['alarm']
			
			for alarme in produto_alarmes['alarmes']:
				contador = contador + 1
				no_alarme = domain.NoHiperbolico()
				no_alarme.id = contador
				no_alarme.name = alarme.alm_nome.encode('utf-8')
				no_alarme.dim = 5
				no_alarme.type = 'circle'
				if alarme.alm_status == 'W':
					no_alarme.color = util.colors['warning']
				elif alarme.alm_status == 'A':
					no_alarme.color = util.colors['alarm']
				
				
				monitores = monitor_repository.get_monitores_alarmando_por_alarme_id(alarme.alm_id)
				
				#pego contagem dos eventos
				for monitor in monitores:
					eventos = monitor_repository.get_eventos_por_monitor_id(monitor.mon_id)
					c = len(eventos)
					if c > maior:
						maior = c
					if c < menor:
						menor = c
					eventos_count[monitor.mon_id] = c
				
				
				#pego os monitores do alarme e adiciono na arvore
				for monitor in monitores:
					contador = contador + 1
					no_monitor = domain.NoHiperbolico()
					no_monitor.id = contador
					no_monitor.name = monitor.mon_nome.encode('utf-8')
					#calculo do diametro a partir do numero de eventos
					razao = float(eventos_count[monitor.mon_id]) / float(maior)
					#print 'mon_id: %s - razao: %.3f' % (monitor.mon_id, razao)
					if razao < 0.05:
						#print 'mon_id: %s - proporcao de erros menor que 5%%' % monitor.mon_id
						no_monitor.dim = 2
					else:
						no_monitor.dim = razao * dim_maximo
						#print 'mon_id: %s - diametro: %.3f' % (monitor.mon_id, no_monitor.dim)
					if monitor.mon_status == 'W':
						no_monitor.color = util.colors['warning']
					elif monitor.mon_status == 'A':
						no_monitor.color = util.colors['alarm']
					
					#adiciono filho(monitor no alarme)
					no_alarme.add_children(copy.deepcopy(no_monitor))
					
				#adiciono filho(alarme no produto)
				no_produto.add_children(copy.deepcopy(no_alarme))
				
			#adiciono filho
			raiz.add_children(copy.deepcopy(no_produto))
			contador = contador + 1
		
		print 'eventos count:\n %s\n' % eventos_count
		print 'maior: %s' % maior
		print 'menor: %s' % menor
		print 'total de eventos: %s' % len(eventos_count)
		return raiz