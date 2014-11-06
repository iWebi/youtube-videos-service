import json
import os

__author__ = 'suman'


def get_json_from_request_body(request):
    return json.loads(request.body)


def flatten_list(inp_list):
    return [item for sublist in inp_list for item in sublist]


def load_file(file_name):
    data = open(os.path.dirname(__file__) + '/' + file_name)
    content = json.load(data)
    data.close()
    return content