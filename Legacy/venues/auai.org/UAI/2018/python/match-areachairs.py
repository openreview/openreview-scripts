#!/usr/bin/python

import argparse
import openreview
import openreview_matcher

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

label = 'areachairs'

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
            'minusers': 1,
            'maxusers': 1,
            'minpapers': 1,
            'maxpapers': 10,
            'alternates': 5,
            'weights': {
                'tpms_score': 1,
                'conflict_score': 1,
                'bid_score': 1
            }
        },
        'constraints': {},
        'paper_invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'metadata_invitation': 'auai.org/UAI/2018/-/Paper_Metadata',
        'assignment_invitation': 'auai.org/UAI/2018/-/Paper_Assignment',
        'match_group': 'auai.org/UAI/2018/Senior_Program_Committee',
        'status': 'complete' # 'queued', 'processing', 'complete' or 'error'
    }
}

configuration_note, assignments = openreview_matcher.match(client, configuration_note_params)

posted_config = client.post_note(configuration_note)

for n in assignments:
    print "posting assignment for ", n.forum
    client.post_note(n)
