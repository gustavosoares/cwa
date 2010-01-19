# coding=utf-8
from django.contrib import admin
from puc.modelo.models import Modelo, VisaoRelatorio, VisaoHierarquica, Widget
from puc.modelo.forms import MyModeloAdminForm
from puc.modelo.repository import ModeloRepository, WidgetRepository
from puc.core import json


class ModeloAdmin(admin.ModelAdmin):
	"""Para o funcionamento desejado na interface administrativa do django, foi preciso reescrever
	os metodos add_view e o change_view, para que fosse possivel adicionar a area onde o pesquisador
	poderá criar os modelos"""
	
	list_display = ('nome', 'descricao', 'metadado', 'estado')
	form = MyModeloAdminForm
	
	def save_model(self, request, obj, form, change):
		"""metodo save_model reescrito para permitir apenas um modelo com estado de ativo"""
		
		print '### salvando o modelo'
		if obj.estado:
			modelos_ativados = Modelo.objects.filter(estado=1)
			if modelos_ativados:
				print '[ModeloAdmin] modelos ativados: %s' % modelos_ativados
				for modelo in modelos_ativados:
					if modelo.id != obj.id:
						Modelo.objects.filter(id=modelo.id).update(estado=0)
						print '##### modelo %s desativado' % modelo
			else:
				print '[ModeloAdmin] nao existe nenhum modelo ativado'
			
		obj.save()
	
	def add_view(self, request, form_url='', extra_context=None):
		"""The 'add' admin view for this model."""
		print '##add view personalizada'
		if request.method == 'POST':
			print '##POST: %s' % request.POST
		
		my_context = { 'mostrar_escolha_modelos' : True }
		return super(ModeloAdmin, self).add_view(request, form_url, extra_context=my_context)


	def change_view(self, request, object_id, extra_context=None):
		"The 'change' admin view for this model."
		print '###change view personalizado'
		modelo_repository = ModeloRepository()
		widget_repository = WidgetRepository()
		modelo = modelo_repository.get_modelo_por_id(object_id)
		widgets = widget_repository.get_todos()
		print 'widgets: %s' % widgets
		modelo_settings_json = modelo_repository.get_modelo_settings(modelo.nome)
		
		my_context = { 'modelo_settings_json' : modelo_settings_json, 
		 'my_widgets' : widgets,
		 'mostrar_escolha_modelos' : True }
		
		return super(ModeloAdmin, self).change_view(request, object_id, extra_context=my_context)

class VisaoRelatorioAdmin(admin.ModelAdmin):
	"""Para o funcionamento desejado na interface administrativa do django, foi preciso reescrever
	os metodos add_view e o change_view, para que fosse possivel adicionar a area onde o pesquisador
	poderá criar os modelos"""

	list_display = ('formato',)
	save_on_top = True
	actions_on_top = False
	actions_on_bottom = False
	
	def add_view(self, request, form_url='', extra_context=None):
		"""The 'add' admin view for this model."""
		print '##[VisaoRelatorio] add view personalizada'
		my_context = { 'mostrar_escolha_modelos' : False }
		
		return super(VisaoRelatorioAdmin, self).add_view(request, form_url, extra_context=my_context)

	def change_view(self, request, object_id, extra_context=None):
		"""change view especializda para o modelo"""
		
		print '###[VisaoRelatorio] change view especialiazada'
		my_context = { 'mostrar_escolha_modelos' : False }

		return super(VisaoRelatorioAdmin, self).change_view(request, object_id, extra_context=my_context)

	def changelist_view(self, request, extra_context=None):
		"""
		changelist view especializada para suprimir algumas ações desnecessárias
		Não é permitido adicionar nem remover, apenas editar o modelo existente.
		"""
		print '###[VisaoRelatorio] changelist_view personalizada'
		#my_context = { 'apenas_editar' : True, 'actions_on_top' : False, 'actions_on_bottom' : False }
		my_context = { 'apenas_editar' : True }
		
		
		return super(VisaoRelatorioAdmin, self).changelist_view(request, extra_context=my_context)
		

class VisaoHierarquicaAdmin(admin.ModelAdmin):
	"""
	configuracao da visao hierarquica. permite ao pesquisador configurar o tempo de atualizacao
	da arvore hiperbolica
	"""

	list_display = ('frequencia_atualizacao',)
	save_on_top = True
	actions_on_top = False
	actions_on_bottom = False

	def add_view(self, request, form_url='', extra_context=None):
		"""The 'add' admin view for this model."""
		print '##[VisaoHierarquicaAdmin] add view personalizada'
		my_context = { 'mostrar_escolha_modelos' : False }

		return super(VisaoHierarquicaAdmin, self).add_view(request, form_url, extra_context=my_context)

	def change_view(self, request, object_id, extra_context=None):
		"""change view especializda para o modelo"""

		print '###[VisaoHierarquicaAdmin] change view especialiazada'
		my_context = { 'mostrar_escolha_modelos' : False }

		return super(VisaoHierarquicaAdmin, self).change_view(request, object_id, extra_context=my_context)

	def changelist_view(self, request, extra_context=None):
		"""
		changelist view especializada para suprimir algumas ações desnecessárias
		Não é permitido adicionar nem remover, apenas editar o modelo existente.
		"""
		print '###[VisaoRelatorio] changelist_view personalizada'
		#my_context = { 'apenas_editar' : True, 'actions_on_top' : False, 'actions_on_bottom' : False }
		my_context = { 'apenas_editar' : True }


		return super(VisaoHierarquicaAdmin, self).changelist_view(request, extra_context=my_context)

class WidgetAdmin(admin.ModelAdmin):
	"""Widget com as visoes"""

	list_display = ('nome', 'descricao', 'url', 'width', 'height',)
	save_on_top = True
	actions_on_top = False
	actions_on_bottom = False

admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(VisaoHierarquica, VisaoHierarquicaAdmin)
admin.site.register(VisaoRelatorio, VisaoRelatorioAdmin)

admin.site.index_template = 'admin/modelo/index.html'
