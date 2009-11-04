"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
	
	def test_geracao_arvore_hiperbolica(self):
		"""
		Testa geracao da arvore hiperbolica
		"""
		response = self.client.get('/hiperbolica/')
		self.failUnlessEqual(response.status_code, 200)



