import openreview
import requests
import os
import json
import re
from import_user import *
client = openreview.Client()
print client.baseurl

def files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            yield filename

directory = '../data/researcher'

f = files(os.path.join(directory,'json'))

errors = {
    'bad_json': [],
    'bad_filename': [],
    'missing_name': []
}

def move(filename, error_type):
	current = os.path.join(directory, 'json', filename)
	new = os.path.join(directory, error_type, filename)
	os.rename(current, new)

for filename in f:
    file_or_id, error_type = import_user(os.path.join(directory, 'json', filename), client)

    if error_type:
        print "FAIL: ", file_or_id
        move(filename, error_type)
    else:
        print "OK: ", file_or_id, filename
        move(filename, 'processed')


