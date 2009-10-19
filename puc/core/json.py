from django.utils import simplejson as json

def encode_json(obj):
	return json.dumps(obj)