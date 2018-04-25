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
parser.add_argument('--append', help='label of the assignment to append')
parser.add_argument('--metadata_inv', default='cv-foundation.org/ECCV/2018/Conference/-/Paper_Metadata')
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
            'minusers': minusers,
            'maxusers': maxusers,
            'minpapers': minpapers,
            'maxpapers': maxpapers,
            'alternates': 5,
            'weights': {
                'tpmsScore': 1.0
            }
        },
        'constraints': {},
        'paper_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'metadata_invitation': args.metadata_inv,
        'assignment_invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Assignment',
        'match_group': 'cv-foundation.org/ECCV/2018/Conference/Area_Chairs',
        'status': 'complete' # 'queued', 'processing', 'complete' or 'error'
    }
})

assignments = openreview_matcher.match(client, config_note, append=args.append)

