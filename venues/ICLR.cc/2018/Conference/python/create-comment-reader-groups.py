'''
Creates paper-specific ".*_and_Higher" groups.

This is to restrict readership of private comments (e.g. those intended
for Authors_and_Higher, Reviewers_and_Higher, or Area_Chairs_and_Higher)
to the roles of the specific paper, not of the general conference.

For example: before the change, a comment with readership of
"Reviewers_and_Higher" would be readable by all ICLR 2018 reviewers. Now,
it will be only readable by the reviewers for the specific paper.

This solves the problem where an author who is also a global ICLR 2018
reviewer is able to see comments on his/her own papers intended for
"Reviewers_and_Higher".
'''

import openreview
import argparse

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to:', client.baseurl

blind_submissions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
for n in blind_submissions:
    print n.number
    authors_and_higher = client.post_group(openreview.Group(**{
            'id': 'ICLR.cc/2018/Conference/Paper{number}/Authors_and_Higher'.format(number=n.number),
            'readers': ['ICLR.cc/2018/Conference'],
            'writers': ['ICLR.cc/2018/Conference'],
            'signatures': ['ICLR.cc/2018/Conference','~Super_User1'],
            'signatories': [],
            'members': [
                'ICLR.cc/2018/Conference/Paper{number}/Authors'.format(number=n.number),
                'ICLR.cc/2018/Conference/Paper{number}/Reviewers'.format(number=n.number),
                'ICLR.cc/2018/Conference/Paper{number}/Area_Chair'.format(number=n.number),
                'ICLR.cc/2018/Conference/Program_Chairs',
                'ICLR.cc/2018/Conference'
            ]
        }))
    reviewers_and_higher = client.post_group(openreview.Group(**{
            'id': 'ICLR.cc/2018/Conference/Paper{number}/Reviewers_and_Higher'.format(number=n.number),
            'readers': ['ICLR.cc/2018/Conference'],
            'writers': ['ICLR.cc/2018/Conference'],
            'signatures': ['ICLR.cc/2018/Conference','~Super_User1'],
            'signatories': [],
            'members': [
                'ICLR.cc/2018/Conference/Paper{number}/Reviewers'.format(number=n.number),
                'ICLR.cc/2018/Conference/Paper{number}/Area_Chair'.format(number=n.number),
                'ICLR.cc/2018/Conference/Program_Chairs',
                'ICLR.cc/2018/Conference'
            ]
        }))

    acs_and_higher = client.post_group(openreview.Group(**{
            'id': 'ICLR.cc/2018/Conference/Paper{number}/Area_Chairs_and_Higher'.format(number=n.number),
            'readers': ['ICLR.cc/2018/Conference'],
            'writers': ['ICLR.cc/2018/Conference'],
            'signatures': ['ICLR.cc/2018/Conference','~Super_User1'],
            'signatories': [],
            'members': [
                'ICLR.cc/2018/Conference/Paper{number}/Area_Chair'.format(number=n.number),
                'ICLR.cc/2018/Conference/Program_Chairs',
                'ICLR.cc/2018/Conference'
            ]
        }))
