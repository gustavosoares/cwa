from django.db import models

# Create your models here.
class Modelo(models.Model):
	nome = models.CharField(max_length=100)
	descricao = models.CharField(max_length=500, blank=True, null=True)
	metadado = models.CharField(max_length=800)
	
	def __unicode__(self):
		return u'%s' % self.nome
		
	class Meta:
		ordering = ['nome']
