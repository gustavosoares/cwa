"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
	
	def test_relatorio_index(self):
		response = self.client.get('/relatorio/')
		self.failUnlessEqual(response.status_code, 200)

	def test_relatorio_xml_response(self):
		response = self.client.get('/relatorio/xml?produto=35&alarme=125&monitor=396&data_inicio=2009-09-01&data_fim=2009-11-03')
		self.failUnlessEqual(response.status_code, 200)

	def test_relatorio_xml_content_type(self):
		response = self.client.get('/relatorio/xml?produto=35&alarme=125&monitor=396&data_inicio=2009-09-01&data_fim=2009-11-03')
		self.failUnlessEqual(response.headers['Content-Type'], 'application/xml')
