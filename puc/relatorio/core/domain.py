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
		return self._grafico
	
	def set_grafico(self, value):
		self._grafico = value
	
	def get_xml(self):
		self.test()
		tabela, servidores, variaveis = self.converter_para_tabela()
		self._grafico.tabela = tabela
		self._grafico.servidores = servidores
		self._grafico.variaveis = variaveis
		#retorno o xml do grafico
		return self._grafico.xml

	def converter_para_tabela(self):
		"""
		metodo para converter os eventos para o formato em tabela utilizado pela
		api flash de geração de gráficos.
		
		Exemplo para dar sort no dicionario:
		langs = author.keys()
		langs.sort()

		for language in langs:
				print language,"is the child of",author[language]
		"""
		self.test()
		
		"""
		tabela com os eventos normalizados
		ex: { data_hora: 
			{'a': {'VARIAVEL' : VALOR }}, 
			{'b': {'VARIAVEL' : VALOR }}
			}
		"""
		tabela = {}
		servidores = {}
		variaveis = {}
		#primeira passada para pegar os servidores
		for evento in self.eventos:
			servidor = evento.servidor
			servidores[servidor] = None
		
		servidores = servidores.keys()
		servidores.sort()
		
		#segunda passada para criar a tabela vazia
		for evento in self.eventos:
			data_hora = evento.get_data_hora_formatada()
			servidor = evento.servidor
			if not tabela.has_key(data_hora):
				s = tabela.get(data_hora,{})
				for servidor_aux in servidores:
					s[servidor_aux] = {}
					for ordem,metadado in evento.metadados.items():
						if metadado['tipo'] == 'N':
							descricao = metadado['descricao']
							variaveis[descricao] = None
							#valor = int(metadado['valor'])
							s[servidor_aux][descricao] = None
				tabela[data_hora] = s		

		variaveis = variaveis.keys()
		variaveis.sort()
				
		#terceira passada para popular a tabela
		for evento in self.eventos:
			data_hora = evento.get_data_hora_formatada()
			servidor = evento.servidor
			for ordem,metadado in evento.metadados.items():
				if metadado['tipo'] == 'N':
					descricao = metadado['descricao']
					valor = int(metadado['valor'])
					tabela[data_hora][servidor][descricao] = valor
		
		return tabela, servidores, variaveis

	
	def test(self):
		"""metodo de validacao"""
		assert self.produto != None, 'produto nao foi definido'
		assert self.alarme != None, 'alarme nao foi definido'
		assert self.monitor != None, 'monitor nao foi definido'
		assert self.eventos != None, 'eventos nao foi definido'
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
		"""retorna o html do relatorio apenas se nao ocorrer nenhum erro nas assertivas"""
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
	"""construtor do relatorio grafico de linha"""
	def __init__(self):
		"""docstring for __init__"""
		from puc.relatorio.core import factory
		Relatorio.__init__(self)
		self.formato = 'grafico_linha'
		self.template_name = 'relatorio/formato/grafico_linha.html'
		self._grafico = factory.GraficoFactory.get_grafico('linha')

	def get_html(self):
		"""retorna o html do relatorio apenas se nao ocorrer nenhum erro nas assertivas"""
		self.test()
		html_grafico = self._grafico.html()
		html_relatorio = render_to_string(self.template_name, {
		'produto' : self.produto,
		'alarme' : self.alarme,
		'monitor' : self.monitor,
		'html_grafico' : html_grafico})
		
		return html_relatorio

class RelatorioGraficoBarra(RelatorioGraficoLinha):
	"""construtor do relatorio grafico de barra"""
	def __init__(self):
		"""docstring for __init__"""
		from puc.relatorio.core import factory
		RelatorioGraficoLinha.__init__(self)
		self.formato = 'grafico_barra'
		self.template_name = 'relatorio/formato/grafico_barra.html'
		self._grafico = factory.GraficoFactory.get_grafico('barra')

	def get_html(self):
		"""retorna o html do relatorio apenas se nao ocorrer nenhum erro nas assertivas"""
		self.test()
		html_grafico = self._grafico.html()
		html_relatorio = render_to_string(self.template_name, {
		'produto' : self.produto,
		'alarme' : self.alarme,
		'monitor' : self.monitor,
		'html_grafico' : html_grafico})

		return html_relatorio
				
class Grafico(object):
	"""interface para o grafico"""
	def __init__(self):
		self.license = "FT421-71A.E2AT5D8RJ4.B-4ZRMDVL"
		self.width = '800'
		self.height = '600'
		self.name = 'grafico-relatorio'
		self.type = None
		self.bgcolor = '#666666'
		self.library_path = '/media/swf/charts_library'
		self.src = "/media/swf/charts.swf"
		self.scale = "noscale" 
		self.align = "middle"
		self.response_type = "application/x-shockwave-flash"
		self.tabela = {} 
		self.servidores = []
		self.variaveis = []
		self._xml = None
		self.xml_source = "/relatorio/xml"
		self.valor_maximo = 0
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
		

	def get_xml(self):
		"""retorna o xml para o grafico"""
		assert 0, 'o metodo para obtencao do xml precisa ser implementado'
	
	xml = property(get_xml)
	
	def get_xml_header(self):
		"""retorna o cabeçalho do xml"""
		
		xml_header = '''
<chart>
	<license>%s</license>
	
	<legend transition='dissolve'
		delay='0'
		bullet='circle'
		size='12'
		/>
	<axis_category skip='1'
		size='12' 
		alpha='85' 
		shadow='medium' 
		orientation='diagonal_up'/>
		
	<axis_value shadow='medium'
	    max='%s'
		min='-40' 
		size='10' 
		color='ffffff' 
		alpha='65' 
		steps='6' 
		show_min='false' />
			
	<axis_ticks value_ticks='false' 
		category_ticks='true' 
		major_thickness='2' 
		minor_thickness='1' 
		minor_count='1' 
		minor_color='222222' 
		position='inside' />
	<chart_type>%s</chart_type>
	
	<chart_guide horizontal='true'
		vertical='true'
		thickness='1' 
		color='ff4400' 
		alpha='75' 
		type='dashed' 

		radius='8'
		fill_alpha='0'
		line_color='ff4400'
		line_alpha='75'
		line_thickness='4'

		size='10'
		text_color='ffffff'
		background_color='ff4400'
		text_h_alpha='90'
		text_v_alpha='90' 
		/>
		<chart_label position='cursor' />

	<chart_rect
		   y='100'
		/>

	<chart_data>\n
		''' % (self.license, (self.valor_maximo * 1.05), self.type)
		
		return xml_header

	def get_xml_footer(self):
		"""retorna o rodapé do xml"""
		xml_footer = '''
	</chart_data>
</chart>
		'''
		return xml_footer
	
	def html(self):
		"""retorna a tag html embed do grafico"""
		
		html = """<EMBED src="%s" FlashVars="library_path=%s&xml_source=%s%%3F%s" 
		quality="high" bgcolor="%s" width="%s" height="%s" NAME="%s" id="%s "allowScriptAccess="sameDomain" 
		swLiveConnect="true" loop="false" scale="%s" salign="TL" align="middle" wmode="opaque"	TYPE="%s" allowFullScreen="true" 
		PLUGINSPAGE="http://www.macromedia.com/go/getflashplayer"/>""" % (self.src, self.library_path, self.xml_source, self.xml_http_get(),
		self.bgcolor, self.width, self.height, self.name, self.name, 
		self.scale, self.response_type)
		
		return html

class GraficoLinha(Grafico):
	"""grafico de linha"""
	def __init__(self):
		Grafico.__init__(self)
		self.type = 'line'

	def get_xml(self):
		"""retorna o xml para o grafico"""
		assert len(self.servidores) > 0, 'nenhum servidor para geracao do grafico está vazia'
		assert len(self.variaveis) > 0, 'nenhuma variavel para geracao do grafico está vazia'

		if self._xml:
			return self._xml
		else:
			
			body = []

			#primeira linha da tabela
			body.append('<row>\n')
			body.append('\t\t<null/>\n')

			horas = self.tabela.keys()
			horas.sort()

			for data_hora in horas:
				body.append('\t\t<string>%s</string>\n' % data_hora)

			body.append('</row>\n')

			#demais linhas

			for servidor in self.servidores:
				for variavel in self.variaveis:
					chart_label = '%s - %s' % (servidor, variavel)
					chart_label = chart_label.encode('utf-8')
					body.append('\t<row>\n')
					body.append('\t\t<string>%s</string>\n' % chart_label)
					for data_hora in horas:
						y = self.tabela[data_hora][servidor][variavel]
						if y:
							if y > self.valor_maximo:
								self.valor_maximo = y
							body.append('\t\t<number tooltip="%s">%s</number>\n' % (y, y))
						else:
							body.append('\t\t<null/>\n')
					body.append('\t</row>\n')

			body = ''.join(body)
			#fim
			header = self.get_xml_header()
			footer = self.get_xml_footer()

			self._xml = header + body + footer
			return self._xml

	xml = property(get_xml)

		
class GraficoBarra(GraficoLinha):
	"""grafico de barra"""
	def __init__(self):
		GraficoLinha.__init__(self)
		self.type = 'column'
