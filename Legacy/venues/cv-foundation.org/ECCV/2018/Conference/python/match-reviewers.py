#!/usr/bin/python

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

print("connecting to {}".format(client.baseurl))

config_note = openreview.Note(**{
    'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Assignment_Configuration',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': ['cv-foundation.org/ECCV/2018/Conference'],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'content': {
        'label': args.label,
        'configuration': {
            'minusers': 3,
            'maxusers': 3,
            'minpapers': 0,
            'maxpapers': 8,
            'alternates': 5,
            'weights': {
                'tpmsScore': 1.0,
                'acRecommendation': 3.0
            }
        },
        'constraints': {},
        'paper_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'metadata_invitation': 'cv-foundation.org/ECCV/2018/Conference/Reviewers/-/Paper_Metadata',
        'assignment_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Assignment',
        'match_group': 'cv-foundation.org/ECCV/2018/Conference/Reviewers',
        'status': 'complete' # 'queued', 'processing', 'complete' or 'error'
    }
})

assignments = openreview_matcher.match(client, config_note)
