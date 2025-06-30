import openreview
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

groups = openreview.tools.build_groups('cv-foundation.org/ECCV/2018/Conference')
for g in groups:
    client.post_group(g)

reviewers_group = client.post_group(openreview.Group(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Reviewers',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['~Super_User1'],
    'signatories': [],
    'members': []
}))

areachairs_group = client.post_group(openreview.Group(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Area_Chairs',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['~Super_User1'],
    'signatories': [],
    'members': []
}))

programchairs_group = client.post_group(openreview.Group(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Program_Chairs',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['~Super_User1'],
    'signatories': [],
    'members': []
}))

submission_invitation = client.post_invitation(openreview.Invitation(id='cv-foundation.org/ECCV/2018/Conference/-/Submission',
    **{
    'duedate': 2515811930000,
    'readers': ['everyone'],
    'writers': [],
    'invitees': ['~'],
    'signatures': ['~Super_User1'],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['cv-foundation.org/ECCV/2018/Conference/Program_Chairs']
        },
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values': ['~Super_User1']
        },
        'writers': {
            'values': []
        },
        'content':{
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.*',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names. Please provide real names; identities will be anonymized.',
                'order': 2,
                'values-regex': ".*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile. Please provide real emails; identities will be anonymized.',
                'order': 3,
                'values-regex': ".*",
                'required':True
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 4,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'subject areas': {
                'description': 'List of subject areas.',
                'order': 5,
                'values-regex': ".*",
                'required':False
            },
            'paperId': {
                'description': 'ECCV paper Id',
                'order': 6,
                'value-regex': ".*",
                'required':True
            }
        }
    }
}))
