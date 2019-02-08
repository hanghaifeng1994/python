import json
from django.http import HttpResponse

def render_json(dictionary={}):
    if type(dictionary) is not dict:
        dictionary = {
            'result':True,
            'message':dictionary,
        }
    return HttpResponse(json.dumps(dictionary), content_type='application/json')