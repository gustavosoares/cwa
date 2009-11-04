"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
	
	def test_sme2_index(self):
		response = self.client.get('/sme2/')
		self.failUnlessEqual(response.status_code, 200)



