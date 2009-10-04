from django.contrib import admin
#from django.contrib.auth.models import User
from puc.sme.models import Monitor, Monitorhelp, Alarme, Produto, Sme

class MonitorAdmin(admin.ModelAdmin):
	list_display = ('mon_id', 'mon_nome', 'mon_tabela', 'mon_status', 'alm_id', 'mon_alarmar')
	search_fields = ('alm_id',)
	list_filter = ('alm_id', 'mon_nome',)
	ordering = ('-alm_id',)

class MonitorhelpAdmin(admin.ModelAdmin):
	list_display = ('mem_id', 'mon_id')
	list_filter = ('mon_id',)
	ordering = ('-mon_id',)

class AlarmeAdmin(admin.ModelAdmin):
	list_display = ('alm_id', 'alm_nome', 'prd_id', 'alm_status', 'alm_alarmar')
	search_fields = ('prd_id',)
	list_filter = ('alm_status', 'prd_id', 'alm_nome', )
	ordering = ('-alm_nome',)

class ProdutoAdmin(admin.ModelAdmin):
	list_display = ('prd_id', 'prd_nome', 'prd_sigla', 'prd_status', 'prd_alarmar',)
	search_fields = ('prd_nome',)
	list_filter = ('prd_nome', 'prd_status', 'prd_sigla')
	ordering = ('-prd_nome',)


admin.site.register(Monitor, MonitorAdmin)
admin.site.register(Monitorhelp, MonitorhelpAdmin)
admin.site.register(Alarme, AlarmeAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Sme)