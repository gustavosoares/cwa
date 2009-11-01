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
		raiz = domain.NoHiperbolico()

		raiz.id = 0
		raiz.name = 'produto'
		
		contador = 1
		#pega os produtos alarmando
		produtos_alarmes = produto_repository.get_produtos_e_seus_alarmes()
		print 'produtos e alarmes alarmando:\n %s\n' % produtos_alarmes
		for produto_alarmes in produtos_alarmes:
			#checo estado do produto
			no_produto = domain.NoHiperbolico()
			no_produto.id = contador
			no_produto.name = produto_alarmes['produto'].prd_nome
			no_produto.dim = 7
			if produto_alarmes['produto'].prd_status == 'W':
				no_produto.color = util.colors['warning']
			elif produto_alarmes['produto'].prd_status == 'A':
				no_produto.color = util.colors['alarm']
			
			for alarme in produto_alarmes['alarmes']:
				contador = contador + 1
				no_alarme = domain.NoHiperbolico()
				no_alarme.id = contador
				no_alarme.name = alarme.alm_nome
				no_alarme.dim = 6
				if alarme.alm_status == 'W':
					no_alarme.color = util.colors['warning']
				elif alarme.alm_status == 'A':
					no_alarme.color = util.colors['alarm']
				
				#pego os monitores do alarme
				monitores = monitor_repository.get_monitor_alarmando_por_alarme_id(alarme.alm_id)
				for monitor in monitores:
					contador = contador + 1
					no_monitor = domain.NoHiperbolico()
					no_monitor.id = contador
					no_monitor.name = monitor.mon_nome
					no_monitor.dim = 5
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
			
			#descomentar se precisar debugar para limitar o tamanho da arvore
			#if len(raiz.children) > 2:
				#break
		
		return raiz