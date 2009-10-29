#-*- coding:utf-8 -*-
from django.template.loader import render_to_string
from puc.sme2.core import util

class Relatorio(object):
	"""Interface dos tipos de relatorios possiveis"""
	def __init__(self):
		self.formato = None
		self.eventos = None
		self._grafico = None
		self.descricao_colunas = None
		self.template_name = None
		self.produto = None
		self.alarme = None
		self.monitor = None
		
	def get_html(self):
		"""retorna a tabela no formato html"""
		assert 0, 'get_html nao foi implementado'
		#raise NotImplementedError
	
	def get_grafico(self):
		assert self._grafico != None, 'o objeto grafico é nulo!'
		return self._grafico
	
	def set_grafico(self, value):
		self._grafico = value
	
	def get_xml(self):
		self.test()
		
		for evento in self.eventos:
			data_hora = evento.get_data_hora_formatada()
			servidor = evento.servidor
			for ordem,metadado in evento.metadados.items():
				if metadado['tipo'] == 'N':
					descricao = metadado['descricao']
					valor = metadado['valor']
					#crio variaveis no xml (cria apenas se nao existe)
					#print '[Relatorio] servidor: %s ' % servidor
					#print '[Relatorio] descricao: %s' % descricao.encode('utf-8')
					variavel = '%s - %s' % (servidor, descricao)
					variavel = variavel.encode('utf-8')
					#print '[Relatorio] variavel: %s' % variavel
					self._grafico.cria_variavel(variavel)
					
					#adiciono os pontos ao xml
					self._grafico.add_ponto(variavel, data_hora, int(valor))
					
		#retorno o xml do grafico
		return self._grafico.xml
	
	def test(self):
		"""metodo de validacao"""
		assert self.produto != None, 'produto nao foi definido'
		assert self.alarme != None, 'alarme nao foi definido'
		assert self.monitor != None, 'monitor nao foi definido'
		assert self.eventos != None, 'eventos nao foi definido'
		#assert len(self.eventos) > 0, 'não há eventos para processar'
		assert self.descricao_colunas != None, 'descricao da colunas nao foi definido'
		assert self.template_name != None, 'nome do template nao foi definido'

	grafico = property(get_grafico, set_grafico)

		
class RelatorioTabular(Relatorio):
	
	def __init__(self):
		"""docstring for __init__"""
		Relatorio.__init__(self)
		self.formato = 'tabular'
		self.template_name = 'relatorio/formato/tabela.html'
	
	def get_html(self):
		self.test()
		html_relatorio = render_to_string(self.template_name, {
		'produto' : self.produto,
		'alarme' : self.alarme,
		'monitor' : self.monitor,
		'colunas_desc' : self.descricao_colunas,
		'eventos' : self.eventos,
		'colors' : util.colors})
		
		return html_relatorio

class RelatorioGraficoLinha(Relatorio):
	"""relatorio grafico de linha"""
	def __init__(self):
		"""docstring for __init__"""
		from puc.relatorio.core import factory
		Relatorio.__init__(self)
		self.formato = 'grafico_linha'
		self.template_name = 'relatorio/formato/grafico_linha.html'
		self._grafico = factory.GraficoFactory.get_grafico('linha')

	def get_html(self):
		"""retorna o html do relatorio"""
		self.test()
		html_grafico = self._grafico.html()
		html_relatorio = render_to_string(self.template_name, {'html_grafico' : html_grafico})
		
		return html_relatorio

class RelatorioGraficoBarra(RelatorioGraficoLinha):
	"""relatorio grafico de barra"""
	def __init__(self):
		"""docstring for __init__"""
		from puc.relatorio.core import factory
		RelatorioGraficoLinha.__init__(self)
		self.formato = 'grafico_barra'
		self.template_name = 'relatorio/formato/grafico_barra.html'
		self._grafico = factory.GraficoFactory.get_grafico('barra')

	def get_html(self):
		"""retorna o html do relatorio"""
		return self._grafico.html()
				
class Grafico(object):
	"""interface para o grafico"""
	def __init__(self):
		self.license = "FT421-71A.E2AT5D8RJ4.B-4ZRMDVL"
		self.width = '800'
		self.height = '650'
		self.name = 'grafico-relatorio'
		self.type = None
		self.bgcolor = '#666666'
		self.library_path = '/media/swf/charts_library'
		self.src = "/media/swf/charts.swf"
		#self.xml_source = '/media/xml/sample.xml'
		self.scale = "noscale" 
		self.align = "middle"
		self.response_type = "application/x-shockwave-flash"
		self.pontos = {} 
		#Ex.: pontos = {'variavel'= {'x' = [0,1,2],'y' = [1,2,3]}}
		self._xml = None
		self.xml_source = "/relatorio/xml"
		
		#atributos usados para montar a url para dar get
		self.produto_id = None
		self.alarme_id = None
		self.monitor_id = None
		self.data_inicio = None
		self.data_fim = None

	def __str__(self):
		return u'grafico: %s' % self.type
	
	def xml_http_get(self):
		"""retorna os parametros do get para gerar o xml de geracao do grafico"""
		s = 'produto=%s&alarme=%s&monitor=%s&data_inicio=%s&data_fim=%s' % (self.produto_id, 
		self.alarme_id, self.monitor_id, self.data_inicio, self.data_fim)
		
		s_encoded = s.replace('&','%26')
		print 'xml http get: %s' % s
		print 'xml http get encoded: %s' % s_encoded
		
		return s_encoded
	
	def cria_variavel(self, variavel):
		"""cria uma variavel no grafico"""
		assert 0, 'o metodo para criacao de uma variavel no grafico precisa ser implementado'
	
	def add_ponto(self, variavel, *args):
		"""adiciona um ponto no grafico"""
		assert 0, 'o metodo para criacao de uma variavel no grafico precisa ser implementado'
		
	def get_xml(self):
		"""retorna o xml para o grafico"""
		assert 0, 'o metodo para obtencao do xml nao foi implementado'
		#raise NotImplementedError
	
	xml = property(get_xml)
	
	def html(self):
		"""retorna a tag html embed do grafico"""
		
		html = """<EMBED src="%s" FlashVars="library_path=%s&xml_source=%s%%3F%s" 
		quality="high" bgcolor="%s" width="%s" height="%s" NAME="%s" id="%s "allowScriptAccess="sameDomain" 
		swLiveConnect="true" loop="false" scale="%s" salign="TL" align="middle" wmode="opaque"  TYPE="%s" allowFullScreen="true" 
		PLUGINSPAGE="http://www.macromedia.com/go/getflashplayer"/>""" % (self.src, self.library_path, self.xml_source, self.xml_http_get(),
		self.bgcolor, self.width, self.height, self.name, self.name, 
		self.scale, self.response_type)
		
		return html

class GraficoLinha(Grafico):
	"""grafico de linha"""
	def __init__(self):
		Grafico.__init__(self)
		self.type = 'line'

	def cria_variavel(self, variavel):
		"""cria uma variavel no grafico"""
		assert variavel != None, "por favor especificar o nome da variavel"
		assert len(variavel) > 0, "por favor especificar o nome da variavel"
		if not self.pontos.has_key(variavel):
			print '## [Grafico] criando variavel: %s' % variavel
			var = self.pontos.get(variavel,{})
			x_aux = var.get('x',[])
			y_aux = var.get('y',[])
			var['x'] = x_aux
			var['y'] = y_aux
			self.pontos[variavel] = var
		
	def add_ponto(self, variavel, x, y):
		"""adiciona um ponto no grafico"""
		x_aux = self.pontos[variavel]['x']
		y_aux = self.pontos[variavel]['y']
		x_aux.append(x)
		y_aux.append(y)
		self.pontos[variavel]['x'] = x_aux
		self.pontos[variavel]['y'] = y_aux
	
	def get_xml(self):
		#print '\n##[GraficoLinha] pontos: \n%s\n' % self.pontos
		assert len(self.pontos) > 0, 'nenhum ponto existe no grafico'
		if self._xml:
			return self._xml
		else:
			header = '''
<chart>
	<license>%s</license>
	<axis_category size='12' 
		alpha='85' 
		shadow='medium' 
		orientation='diagonal_up'/>
	<axis_ticks value_ticks='false' 
		category_ticks='true' 
		major_thickness='2' 
		minor_thickness='1' 
		minor_count='1' 
		minor_color='222222' 
		position='inside' />
	<axis_value shadow='medium' 
		min='-40' 
		size='10' 
		color='ffffff' 
		alpha='65' 
		steps='6' 
		show_min='false' />
	<chart_type>%s</chart_type>
	<chart_data>\n
			''' % (self.license, self.type)
		
			body = []
			#eixo x
			body.append('<row>\n')
			body.append('\t\t<null/>\n')
			print 'pontos no grafico: %s ' % self.pontos
			#Ex.: pontos = {'variavel'= {'x' = [0,1,2],'y' = [1,2,3]}}
			for var, pontos in self.pontos.items():
				x_axis = self.pontos[var]['x']
				#print 'x_axis: %s' % x_axis
				for x in x_axis:
					body.append('\t\t<string>%s</string>\n' % x)
				break #break para gerar o grafico da primeira variavel
		
			body.append('\t</row>\n')
		
			#eixo y
			for var, pontos in self.pontos.items():
				if var == 'null':
					continue
				body.append('\t<row>\n')
				body.append('\t\t<string>%s</string>\n' % var)
				y_axis = self.pontos[var]['y']
				for y in y_axis:
					body.append('\t\t<number tooltip="%s">%s</number>\n' % (y, y))
				body.append('\t</row>\n')
				break #break para gerar grafico da primeira variavel
			
			body = ''.join(body)
			#fim
			footer = '\t</chart_data>\n</chart>\n'

			self._xml = header + body + footer
			return self._xml
	
	xml = property(get_xml)

		
class GraficoBarra(GraficoLinha):
	"""grafico de linha"""
	def __init__(self):
		GraficoLinha.__init__(self)
		self.type = 'bar'
