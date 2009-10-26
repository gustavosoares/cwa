from django.contrib import admin
from puc.modelo.models import Modelo

"""Imports tirados do arquivo admin/options.py"""
from django import forms, template
from django.forms.formsets import all_valid
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import widgets
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects, model_ngettext, model_format_dict
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models.fields import BLANK_CHOICE_DASH
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.datastructures import SortedDict
from django.utils.functional import update_wrapper
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.functional import curry
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext, ugettext_lazy
from django.utils.encoding import force_unicode
try:
    set
except NameError:
    from sets import Set as set     # Python 2.3 fallback



class ModeloAdmin(admin.ModelAdmin):
	
	def add_view(self, request, form_url='', extra_context=None):
		print 'add vieww personalizada'
		"The 'add' admin view for this model."
		model = self.model
		opts = model._meta

		if not self.has_add_permission(request):
			raise PermissionDenied

		ModelForm = self.get_form(request)
		formsets = []
		if request.method == 'POST':
			print 'POST: %s' % request.POST
			form = ModelForm(request.POST, request.FILES)
			if form.is_valid():
				form_validated = True
				print 'FORM: %s' % form
				new_object = self.save_form(request, form, change=False)
			else:
				form_validated = False
				new_object = self.model()
			prefixes = {}
			for FormSet in self.get_formsets(request):
				prefix = FormSet.get_default_prefix()
				prefixes[prefix] = prefixes.get(prefix, 0) + 1
				if prefixes[prefix] != 1:
					prefix = "%s-%s" % (prefix, prefixes[prefix])
				formset = FormSet(data=request.POST, files=request.FILES,
								  instance=new_object,
								  save_as_new=request.POST.has_key("_saveasnew"),
								  prefix=prefix)
				formsets.append(formset)
			if all_valid(formsets) and form_validated:
				self.save_model(request, new_object, form, change=False)
				form.save_m2m()
				for formset in formsets:
					self.save_formset(request, form, formset, change=False)

				self.log_addition(request, new_object)
				return self.response_add(request, new_object)
		else:
			# Prepare the dict of initial data from the request.
			# We have to special-case M2Ms as a list of comma-separated PKs.
			initial = dict(request.GET.items())
			for k in initial:
				try:
					f = opts.get_field(k)
				except models.FieldDoesNotExist:
					continue
				if isinstance(f, models.ManyToManyField):
					initial[k] = initial[k].split(",")
			form = ModelForm(initial=initial)
			prefixes = {}
			for FormSet in self.get_formsets(request):
				prefix = FormSet.get_default_prefix()
				prefixes[prefix] = prefixes.get(prefix, 0) + 1
				if prefixes[prefix] != 1:
					prefix = "%s-%s" % (prefix, prefixes[prefix])
				formset = FormSet(instance=self.model(), prefix=prefix)
				formsets.append(formset)

		adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)), self.prepopulated_fields)
		media = self.media + adminForm.media

		inline_admin_formsets = []
		for inline, formset in zip(self.inline_instances, formsets):
			fieldsets = list(inline.get_fieldsets(request))
			inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
			inline_admin_formsets.append(inline_admin_formset)
			media = media + inline_admin_formset.media

		context = {
			'title': _('Add %s') % force_unicode(opts.verbose_name),
			'adminform': adminForm,
			'is_popup': request.REQUEST.has_key('_popup'),
			'show_delete': False,
			'media': mark_safe(media),
			'inline_admin_formsets': inline_admin_formsets,
			'errors': helpers.AdminErrorList(form, formsets),
			'root_path': self.admin_site.root_path,
			'app_label': opts.app_label,
		}
		context.update(extra_context or {})
		return self.render_change_form(request, context, form_url=form_url, add=True)
	add_view = transaction.commit_on_success(add_view)
	
admin.site.register(Modelo, ModeloAdmin)

#admin.site.index_template = 'modelo/index.html'
