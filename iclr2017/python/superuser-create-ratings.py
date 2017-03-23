## Import statements
import argparse
import csv
import sys
import openreview
import re

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

iclrsubs = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
tildematch = re.compile('~.+')

field_content = {
    'description': 'Rating for this reviewer',
    'order': 1,
    'value-radio': [
        '5. Reviewer feedback was very informative, factually correct and constructive.',
        '4. Reviewer feedback was informative but it contained some factual errors or missing points which were later acknowledged.',
        '3. Reviewer feedback was mostly informative, but not entirely accurate.',
        '2. Reviewer feedback was not very informative.',
        '1. Reviewer feedback was incorrect or reviewer did not seem to have read the paper in enough detail.'
    ]
}

for i in iclrsubs:
    reviewers = client.get_group('ICLR.cc/2017/conference/paper%s/reviewers' % i.number)
    #true_members = []
    #for anonreviewer in reviewers.members:
    #    ar = client.get_group(anonreviewer)
    #    true_members+=[a for a in ar.members if tildematch.match(a)]

    content = {t.split('/')[4]:field_content for t in reviewers.members}
    content['title'] = {
        'description': 'the title of the paper of the reviewers being rated',
        'order':0,
        'value':'Review Rating: '+i.content['title']
    }

    ac_rating_invitation = openreview.Invitation('ICLR.cc/2017/conference/-/paper%s/AC/Review/Rating' % i.number,
        readers = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/paper%s/areachairs' % i.number],
        writers = ['ICLR.cc/2017/conference'],
        signatures = ['ICLR.cc/2017/conference'],
        invitees = ['ICLR.cc/2017/conference/paper%s/areachairs' % i.number],
        process = '../process/ratingProcess.js',
        reply = {
            'content': content,
            'readers': {
                'values': ['ICLR.cc/2017/pcs']
            },
            'signatures': {
                'values-regex': '~.*'
            },
            'writers': {
                'values-regex': '~.*'
            },
            'forum': i.forum,
            'replyto':i.forum
        }
    )

    client.post_invitation(ac_rating_invitation)

    author_rating_invitation = openreview.Invitation(
        'ICLR.cc/2017/conference/-/paper%s/Author/Review/Rating' % i.number,
        readers = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/paper%s/authors' % i.number],
        writers = ['ICLR.cc/2017/conference'],
        signatures = ['ICLR.cc/2017/conference'],
        invitees = ['ICLR.cc/2017/conference/paper%s/authors' % i.number],
        process = '../process/ratingProcess.js',
        duedate = 1485554400000,
        reply = {
            'content': content,
            'readers': {
                'values': ['ICLR.cc/2017/pcs']
            },
            'signatures': {
                'values-regex': '~.*'
            },
            'writers': {
                'values-regex': '~.*'
            },
            'forum': i.forum,
            'replyto':i.forum
        }
    )
    client.post_invitation(author_rating_invitation)



