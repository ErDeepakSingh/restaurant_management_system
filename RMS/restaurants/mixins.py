from django.http import HttpResponse


class HttpResponseMixin(object):
    def render_to_http_response(self,data,status=200):
        return HttpResponse(data,content_type='application/json',status=status)

from django.core.serializers import serialize
import json
class SerializeMixin(object):
    def serialize(self,querry_set):
        json_data=serialize('json',querry_set)
        pdict=json.loads(json_data)
        final_list=[]
        for obj in pdict:
            final_list.append(obj['fields'])
        json_data=json.dumps(final_list)
        return json_data



def is_json(data):
    try:
        real_data=json.loads(data)
        valid=True
    except ValueError:
        valid=False
    return valid