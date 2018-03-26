#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""
from __future__ import print_function
import argparse
import openreview
import openreview_matcher

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--label', required=True)
parser.add_argument('--number')
parser.add_argument('-p', '--paperlimits', nargs=2, required=True, help='Enter two integers: the first should be the minimum number of papers per user, and the second should be the maximum.')
parser.add_argument('-u', '--userlimits', nargs=2, required=True, help='Enter two integers: the first should be the minimum number of users per paper, and the second should be the maximum.')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

print("connecting to {}".format(client.baseurl))

label = args.label
minusers, maxusers = [int(limitstring) for limitstring in args.userlimits]
minpapers, maxpapers = [int(limitstring) for limitstring in args.paperlimits]

print("matching with the following parameters: ")
print("Min/Max users: {}/{}".format(minusers, maxusers))
print("Min/Max papers: {}/{}".format(minpapers, maxpapers))

if args.number:
    config_notes = client.get_notes(
        invitation='cv-foundation.org/ECCV/2018/Conference/-/Assignment_Configuration',
        number=args.number)
else:
    config_notes = client.get_notes(
        invitation='cv-foundation.org/ECCV/2018/Conference/-/Assignment_Configuration')

config_by_label = {n.content['label']: n.to_json() for n in config_notes}

# post the configuration note. in the future, this note will be posted through the UI.

configuration_note_params = {
    'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Assignment_Configuration',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': ['cv-foundation.org/ECCV/2018/Conference'],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'content': {
        'label': label,
        'configuration': {
            'minusers': minusers,
            'maxusers': maxusers,
            'minpapers': minpapers,
            'maxpapers': maxpapers,
            'alternates': 5,
            'weights': {
                'tpms_score': 1,
                'conflict_score': 1
            }
        },
        'constraints': {},
        'paper_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'metadata_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Metadata',
        'assignment_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Assignment',
        'match_group': 'cv-foundation.org/ECCV/2018/Conference/Area_Chairs',
        'status': 'complete' # 'queued', 'processing', 'complete' or 'error'
    }
}

if args.number:
    config_note = openreview.matching.create_or_update_config(client, label, configuration_note_params, number=args.number)
else:
    config_note = openreview.matching.create_or_update_config(client, label, configuration_note_params, number=args.number)

print(config_note.id)
print("config note constraints")
for k,v in config_note.content['constraints'].iteritems():
    print(k,v)

posted_config = client.post_note(config_note)

assignments = openreview.matching.match(client, posted_config, openreview_matcher.Solver)

for n in assignments:
    print("posting assignment for ", n.forum, label)
    client.post_note(n)
