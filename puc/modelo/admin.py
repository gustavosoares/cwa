# coding=utf-8
from django.contrib import admin
from puc.modelo.models import Modelo, VisaoRelatorio
from puc.modelo.forms import MyModeloAdminForm
from puc.modelo.repository import ModeloRepository
from puc.core import json


class ModeloAdmin(admin.ModelAdmin):
	"""Para o funcionamento desejado na interface administrativa do django, foi preciso reescrever
	os metodos add_view e o change_view, para que fosse possivel adicionar a area onde o pesquisador
	poderá criar os modelos"""
	
	list_display = ('nome', 'descricao', 'metadado',)
	form = MyModeloAdminForm
	
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
		modelo = modelo_repository.get_modelo_por_id(object_id)
		modelo_settings_json = modelo_repository.get_modelo_settings(modelo.nome)
		
		my_context = { 'modelo_settings_json' : modelo_settings_json,
		 'mostrar_escolha_modelos' : True }
		
		return super(ModeloAdmin, self).change_view(request, object_id, extra_context=my_context)

class VisaoRelatorioAdmin(admin.ModelAdmin):
	"""Para o funcionamento desejado na interface administrativa do django, foi preciso reescrever
	os metodos add_view e o change_view, para que fosse possivel adicionar a area onde o pesquisador
	poderá criar os modelos"""

	list_display = ('formato',)
	
	def add_view(self, request, form_url='', extra_context=None):
		"""The 'add' admin view for this model."""
		print '##add view personalizada'
		my_context = { 'mostrar_escolha_modelos' : False }
		
		return super(VisaoRelatorioAdmin, self).add_view(request, form_url, extra_context=my_context)

	def change_view(self, request, object_id, extra_context=None):
		"The 'change' admin view for this model."
		print '###change view personalizado'
		my_context = { 'mostrar_escolha_modelos' : False }

		return super(VisaoRelatorioAdmin, self).change_view(request, object_id, extra_context=my_context)

admin.site.register(Modelo, ModeloAdmin)
admin.site.register(VisaoRelatorio, VisaoRelatorioAdmin)

admin.site.index_template = 'admin/modelo/index.html'
