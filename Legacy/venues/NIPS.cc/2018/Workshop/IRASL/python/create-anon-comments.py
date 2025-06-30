#!/usr/bin/python

###############################################################################
# ex. python create-invitations.py --conf MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# To be run after submission due date to create review invitations for all the papers.
# For each paper:
# 1) create authorGroup (can see reviews, can't write a review)
#           reviewer group (reviewers for this paper)
#           and nonReviewerGroup (folks that aren't allowed to read the review at least not yet)
# 2) create review invitation
###############################################################################

## Import statements
import argparse
from openreview import *
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)

blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
for paper in blind_submissions:
    paper_num = str(paper.number)
    paperinv = config.CONFERENCE_ID + '/-/Paper' + paper_num
    paperGroup = config.CONFERENCE_ID + '/Paper' + paper_num
    authorGroup = paperGroup+'/Authors'

    comment_reply = {
        'forum': paper.id,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'writers': [config.CONFERENCE_ID],
        'signatures': {'values-regex': paperGroup+'/AnonReviewer[0-9]+|'+paperGroup+'/Authors|'+config.PROGRAM_CHAIRS+'|~.*'},
        'content': {
            'title': {
                'order': 0,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your comment.',
                'required': True
            },
            'comment': {
                'order': 1,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Your comment or reply (max 5000 characters).',
                'required': True
            }
        }
    }

    comment_parameters = {
        'invitees': ['~'],
        'readers': ['everyone'],
        'writers': [config.CONFERENCE_ID],
        'signatures': [config.CONFERENCE_ID],
        'process': '../process/commentProcess.js',
        'reply': comment_reply
    }

    invite = openreview.Invitation(paperinv + '/Comment', **comment_parameters)
    client.post_invitation(invite)
    print(invite.id)
