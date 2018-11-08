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
import os
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

    ## Official Comment
    comment_parameters = {
        'readers': ['everyone'],
        'writers': [config.PROGRAM_CHAIRS],
        'invitees': [config.PROGRAM_CHAIRS],
        'signatures': [config.PROGRAM_CHAIRS],
        'process': os.path.join(os.path.dirname(__file__), '../process/pcCommentProcess.js')
    }
    comment_parameters['reply'] = {
        'forum': paper.id,
        'replyto': None,
        'writers': {'values': [config.PROGRAM_CHAIRS]},
        'signatures': {'values': [config.PROGRAM_CHAIRS]},
        'readers': {
            'values': [config.PROGRAM_CHAIRS, paperGroup + '/Authors'],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': {
            'comment': {
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Comments to authors. Text up to 5000 chars.',
                'required': True,
            }
        }
    }
    invite = openreview.Invitation(paperinv + '/PC_to_Author_Comment', **comment_parameters)
    client.post_invitation(invite)