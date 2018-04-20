import openreview
import openreview_matcher
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

metadata_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Metadata',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': ['cv-foundation.org/ECCV/2018/Conference'],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'readers': {'values': [
            'cv-foundation.org/ECCV/2018/Conference',
            'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
            ]},
        'writers': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'signatures': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'content': {}
    }
}))

metadata_reviewers_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Reviewers/-/Paper_Metadata',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': ['cv-foundation.org/ECCV/2018/Conference'],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'readers': {'values': [
            'cv-foundation.org/ECCV/2018/Conference',
            'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
            ]},
        'writers': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'signatures': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'content': {}
    }
}))

metadata_acs_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Area_Chairs/-/Paper_Metadata',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': ['cv-foundation.org/ECCV/2018/Conference'],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'readers': {'values': [
            'cv-foundation.org/ECCV/2018/Conference',
            'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
            ]},
        'writers': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'signatures': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'content': {}
    }
}))

print "posting assignment invitation..."
assignment_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Assignment',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': ['cv-foundation.org/ECCV/2018/Conference'],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
        'readers': {'values': [
            'cv-foundation.org/ECCV/2018/Conference',
            'cv-foundation.org/ECCV/2018/Conference/Program_Chairs']
        },
        'writers': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'signatures': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'content': {
        }
    }
}))

print "posting configuration invitation..."
config_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/-/Assignment_Configuration',
    'readers': [
        'cv-foundation.org/ECCV/2018/Conference',
        'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
    ],
    'writers': [
        'cv-foundation.org/ECCV/2018/Conference'
    ],
    'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': None,
        'readers': {'values': [
            'cv-foundation.org/ECCV/2018/Conference',
            'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
        ]},
        'writers': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'signatures': {'values': ['cv-foundation.org/ECCV/2018/Conference']},
        'content': {
        }
    }

}))
