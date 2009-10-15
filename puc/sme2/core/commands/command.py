from puc.core.singleton import Singleton
from puc.sme2.core.commands import listar_projeto


class commandMap(Singleton):
	def __init__(self):
		print 'iniciando command map'
		self.commands = {}
		self.commands['listar_projeto'] = listar_projeto.listarProjetosCommand()



class command():
	
	def __init__(self, name, template):
		self.template = template
		self.name = name
		
	def execute(request, *args, **kwargs):
		pass
		
