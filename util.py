import json

__author__ = 'suman'


def get_json_from_request_body(request):
    return json.loads(request.body)