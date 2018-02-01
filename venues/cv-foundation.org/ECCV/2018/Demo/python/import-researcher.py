import openreview
import requests
import os
import json
import re
import csv
from import_user import *
client = openreview.Client()
print client.baseurl

def Files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            yield os.path.join(directory, filename)

directory = '../data/researcher/processed'

files = Files(directory)

for filename in files:
    resolved_filename = filename.replace('/processed/','/resolved/')
    unresolved_filename = filename.replace('/processed/','/unresolved/')

    if not os.path.isfile(resolved_filename) and not os.path.isfile(unresolved_filename):
        profile_data, resolved = import_user(client, filename)

        if resolved:
            profile_note = openreview.Note(**profile_data)
            p = client.update_profile(profile_note.id, profile_note.content)

            resolved_filename = filename.replace('/processed/','/resolved/')
            print "  resolved: ", filename
            with open(resolved_filename, 'wb') as f:
                f.write(json.dumps(p.to_json()))
        else:
            print "unresolved: ", filename
            with open(unresolved_filename, 'wb') as f, open(filename) as o:
                f.write(o.read())
    else:
        pass

