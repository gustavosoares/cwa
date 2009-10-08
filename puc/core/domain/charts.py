
#
# Chart
#
class Chart:
    def __init__(self):
        self._width = None
        self._height = None
        self._name = 'Chart'
        self._type = None
        self._bgcolor = '#666666'
        self._library_path = '/media/swf/charts_library'
        self._src = "/media/swf/charts.swf"
        #TODO: gerar uma script com o xml
        self._xml_source = '/media/xml/sample.xml'
        self._scale = "noscale" 
        self._align = "middle"
        self._response_type = "application/x-shockwave-flash"

	def get_width(self):
		return self._width

	def get_height(self):
		return self._height

	def get_name(self):
		return self._name

	def get_type(self):
		return self._type

 
class LineChart(Chart):
    def __init__(self):
        self._type = 'line'
 
class BarChart(Chart):
    def __init__(self):
        self._type = 'bar'
 
 
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
	print chart.get_type()

