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
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

label = args.label

# post the configuration note. in the future, this note will be posted through the UI.
configuration_note_params = {
    'invitation': 'auai.org/UAI/2018/-/Assignment_Configuration',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs'
    ],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'content': {
        'label': label,
        'configuration': {
            'minusers': 3,
            'maxusers': 3,
            'minpapers': 2,
            'maxpapers': 5,
            'alternates': 5,
            'weights': {
                'bid_score': 1,
                'tpms_score': 1,
                'conflict_score': 1,
                'recommendation_score': 1
            }
        },
        'constraints': {},
        'paper_invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'metadata_invitation': 'auai.org/UAI/2018/-/Paper_Metadata',
        'assignment_invitation': 'auai.org/UAI/2018/-/Paper_Assignment',
        'constraints_invitation': 'auai.org/UAI/2018/-/Paper_Constraints',
        'match_group': 'auai.org/UAI/2018/Program_Committee',
        'status': 'complete' # 'queued', 'processing', 'complete' or 'error'
    }
}

config_notes = client.get_notes(invitation='auai.org/UAI/2018/-/Assignment_Configuration')
config_note = [c for c in config_notes if c.content['label'] == label][0]
config_note = openreview.Note(**dict(config_note.to_json(), **configuration_note_params))
posted_config = client.post_note(config_note)

assignments = openreview_matcher.match(client, posted_config, openreview_matcher.Solver)

for n in assignments:
    print("posting assignment for ", n.forum)
    client.post_note(n)

