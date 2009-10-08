from chart_xml import chartXml

#
# Chart
#
class Chart:
	def __init__(self):
		self.width = None
		self.height = None
		self.name = 'Chart'
		self.type = type
		self.bgcolor = '#666666'
		self.library_path = '/media/swf/charts_library'
		self.src = "/media/swf/charts.swf"
		#TODO: gerar uma script com o xml
		self.xml_source = '/media/xml/sample.xml'
		self.scale = "noscale" 
		self.align = "middle"
		self.response_type = "application/x-shockwave-flash"
		self.chart_xml = chartXml(self.type)
		
	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def get_name(self):
		return self.name

	def get_type(self):
		return self.type

	def get_bgcolor(self):
		return self.bgcolor

	def get_library_path(self):
		return self.library_path

	def get_src(self):
		return self.src

	def get_xml_source(self):
		return self.xml_source

	def get_scale(self):
		return self.scale

	def get_align(self):
		return self.align

	def get_response_type(self):
		return self.response_type

	def get_chart_xml(self):
		return self.chart_xml

 
class LineChart(Chart):
	def __init__(self):
		Chart.__init__(self)
		self.type = 'line'
		self.chart_xml = chartXml(self.type)
 
class BarChart(Chart):
	def __init__(self):
		Chart.__init__(self)
		self.type = 'bar'
		self.chart_xml = chartXml(self.type)

#
# ChartFactory
#
class ChartFactory:
	@staticmethod
	def create_chart(chart_type):
		if chart_type == 'line':
			return LineChart()
		elif chart_type == 'bar':
			return BarChart()

 
if __name__ == '__main__':
	chart = ChartFactory.create_chart('line')
	#chart = Chart()
	print chart.get_type()
	print chart.get_src()
	
	chart_xml_object = chart.get_chart_xml()
	
	chart_xml_object.create_x_axis()
	chart_xml_object.add_x_axis('2005')
	chart_xml_object.add_x_axis('2006')
	chart_xml_object.add_x_axis('2007')
	chart_xml_object.add_x_axis('2008')
	chart_xml_object.add_x_axis('2009')
	
	chart_xml_object.create_row('region 1')
	chart_xml_object.add_to_row('region 1', '48')
	chart_xml_object.add_to_row('region 1', '55')
	chart_xml_object.add_to_row('region 1', '80')
	chart_xml_object.add_to_row('region 1', '100')
	chart_xml_object.add_to_row('region 1', '90')

	chart_xml_object.create_row('region 2')
	chart_xml_object.add_to_row('region 2', '-12')
	chart_xml_object.add_to_row('region 2', '10')
	chart_xml_object.add_to_row('region 2', '55')
	chart_xml_object.add_to_row('region 2', '65')
	chart_xml_object.add_to_row('region 2', '90')

	chart_xml_object.create_row('region 3')
	chart_xml_object.add_to_row('region 3', '27')
	chart_xml_object.add_to_row('region 3', '-20')
	chart_xml_object.add_to_row('region 3', '15')
	chart_xml_object.add_to_row('region 3', '80')
	chart_xml_object.add_to_row('region 3', '90')

	print chart_xml_object.get_xml()

