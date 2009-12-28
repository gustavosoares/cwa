#-*- coding:utf-8 -*-
from django.template.loader import render_to_string
import datetime
from puc.core import json

class NoHiperbolico(object):
	
	def __init__(self):
		"""construtor"""
		self.id = 0
		self.name = ''
		self.data = {}
		self.children = []
		self.children_dict = {}
		#self.children_json = []
		self.type = 'circle'
		self.color = '#f00'
		self.dim = 10
	
	def add_children(self, no):
		"""
		metodo para adicionar um nó filho
		recebe como parametro um objeto NoHiperbolico
		"""
		'''
		if no in self.children:
			self.children.remove(no)
			
		#self.children.append(str(no))
		self.children.append(no)
		'''
		self.children_dict[no.name] = no
		
	def count_children(self):
		"""counts the number of children"""
		return len(self.children)

	def add_data(self, key, value):
		"""
		permite adicionar um metadado ao nó
		"""
		self.data[key] = value
	
	def __repr__(self):
		#return 'repr -> %s' % self.name
		return self.__str__()

	def __str__(self):
		"""
		método __str__ sobreescrito para retornar um objeto json (string) da
		representacao do objeto
		"""
		dict_ = {}
		
		self.add_data('$color', self.color)
		self.add_data('$dim', self.dim)
		self.add_data('$type', self.type)
		
		dict_['id'] = self.id
		dict_['name'] = self.name
		dict_['data'] = self.data
		
		for key,value in self.children_dict.items():
			self.children.append(str(value))
		
		dict_['children'] = self.children
		
		s = json.encode_json(dict_)
		
		#replaces de lixos no json
		s = s.replace('\\"','"')
		s = s.replace('["{"','[{"')
		s = s.replace('"}"]','"}]')
		s = s.replace('"{"','{"')
		s = s.replace('}",','},')
		return s
		

		#return str(self)

