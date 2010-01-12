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

def elapsed(inicio):
	fim = time.time()
	elapsed = (fim - inicio) / 60
	print '##### Tempo de execução: %f min' % elapsed
	#logging.debug('duracao: %.2f min' % elapsed)
	return elapsed
	
#colors['normal'] = '#006400'
#colors['warning'] = '#DAA520'
#colors['alarm'] = '#DC143C'