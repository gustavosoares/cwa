# coding=utf-8

import time

#definicao das cores utilizadas na console de monitoracao
colors = {
	'normal' : '#006400',
	'warning' : '#DAA520',
	'alarm' : '#DC143C'
}

def start_counter():
	return time.time()

def elapsed(inicio, comando=''):
	fim = time.time()
	#elapsed = (fim - inicio) / 60
	elapsed = (fim - inicio)
	print '##### Tempo de execução [%s]: %f seg' % (comando, elapsed)
	#logging.debug('duracao: %.2f min' % elapsed)
	return elapsed
	
#colors['normal'] = '#006400'
#colors['warning'] = '#DAA520'
#colors['alarm'] = '#DC143C'
