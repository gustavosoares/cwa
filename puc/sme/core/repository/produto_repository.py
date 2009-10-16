
from django.conf import settings
from puc.sme.models import Produto, Alarme, Monitor


def get_produtos():
	return Produto.objects.all()