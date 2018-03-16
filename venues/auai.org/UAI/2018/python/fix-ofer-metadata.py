import requests
import os
import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)


metadata = client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Metadata')
for m in metadata:
    score_entries = m.content['groups']['auai.org/UAI/2018/Senior_Program_Committee']
    ofer_entry = [s for s in score_entries if s['userId'] == '~Ofer_Meshi2']
    if ofer_entry:
        for e in ofer_entry:
            e['userId'] = '~Ofer_Meshi1'
    client.post_note(m)
