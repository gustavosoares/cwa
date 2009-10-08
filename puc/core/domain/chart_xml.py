'''
<row>
	<null/>
	<string>2005</string>
	<string>2006</string>
	<string>2007</string>
	<string>2008</string>
	<string>2009</string>
</row>
<row>
	<string>region 1</string>
	<number shadow='medium' tooltip='$48 Million'>48</number>
	<number tooltip='$55 Million'>55</number>
	<number tooltip='$80 Million'>80</number>
	<number tooltip='$100 Million'>100</number>
	<number tooltip='$90 Million'>90</number>
</row>
'''

class chartXml:
	def __init__(self, type):
		self._rows = {}
		self._x_axis = {}
		self._type = type
		
	def create_row(self, title):
		self._rows[title] = []

	def get_rows(self, title):
		return self._rows

	def get_row(self, title):
		return self._rows[title]
		
	#adiciona valor na linha. O titulo e a regiao
	def add_to_row(self, title, value):
		l = self._rows[title]
		#<number tooltip='$55 Million'>55</number>
		l.append(value)	
	
	#cria o eixo X	
	def create_x_axis(self):
		self.create_row('null')
		
	def add_x_axis(self, value):
		self.add_to_row('null', value)
		
	def get_x_axis(self):
		return self._x_axis
		
	def get_xml(self):
		xml = ''
		#cabecalho
		header = '''
<chart>

	<axis_category size='16' alpha='85' shadow='medium' />
	<axis_ticks value_ticks='false' category_ticks='true' major_thickness='2' minor_thickness='1' minor_count='1' minor_color='222222' position='inside' />
	<axis_value shadow='medium' min='-40' size='10' color='ffffff' alpha='65' steps='6' show_min='false' />
	<chart_type>%s</chart_type>
	<chart_data>\n
''' % self._type
		
		body = []
		#eixo x_axis
		body.append('\t<row>\n')
		body.append('\t\t<null/>\n')
		
		for x_axis in self._rows['null']:
			body.append('\t\t<string>%s</string>\n' % x_axis)
		
		body.append('\t</row>\n')
		#data
		#for k, v in self._row.iteritems():
		for title, points in self._rows.items():
			if title == 'null':
				continue
			body.append('\t<row>\n')
			body.append('\t\t<string>%s</string>\n' % title)
			for point in points:
				body.append('\t\t<number tooltip="%s">%s</number>\n' % (point, point))
			body.append('\t</row>\n')
			
		
		body = ''.join(body)
		#fim
		footer = '\t</chart_data>\n</chart>\n'
		
		xml = header + body + footer
		return xml