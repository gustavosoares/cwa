from django.contrib import admin
from puc.modelo.models import Modelo

class ModeloAdmin(admin.ModelAdmin):
	
	exclude = ('ordem',)
	
	def add_view(self, request, form_url='', extra_context=None):
		print 'add vieww personalizada'
		return admin.ModelAdmin.add_view(self, request, form_url, extra_context)
	
admin.site.register(Modelo, ModeloAdmin)

#admin.site.index_template = 'modelo/index.html'
