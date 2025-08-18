import openreview
import requests
import os
import json
import re
import csv
import logging
from import_user import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('directory')
parser.add_argument('--baseurl', help="openreview base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "connecting to", client.baseurl

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# setup handler
handler = logging.FileHandler('import-researcher.log')
handler.setLevel(logging.INFO)

# create logging format
# edit this
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def Files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            yield os.path.join(directory, filename)

files = Files(args.directory)

resolved_dir = args.directory.replace('/json', '/resolved')
unresolved_dir = args.directory.replace('/json', '/unresolved')
for d in [resolved_dir, unresolved_dir]:
    if not os.path.isdir(d):
        os.mkdir(d)

for filename in files:
    resolved_filename = filename.replace('/json/','/resolved/')
    unresolved_filename = filename.replace('/json/','/unresolved/')

    if not os.path.isfile(resolved_filename) and not os.path.isfile(unresolved_filename):
        profile_data, resolved = import_user(client, filename)

        profile_id = ''
        if resolved:
            profile_note = openreview.Note(**profile_data)
            p = client.update_profile(profile_note.id, profile_note.content)
            profile_id = p.id.encode('utf-8')
            with open(resolved_filename, 'wb') as f:
                f.write(json.dumps(p.to_json()))
        else:
            with open(unresolved_filename, 'wb') as f, open(filename) as o:
                f.write(o.read())
        logger.info('{:10s}{:35s}{:15s}'.format(
            'resolved' if resolved else 'unresolved',
            filename,
            profile_id
            ))
    else:
        pass

