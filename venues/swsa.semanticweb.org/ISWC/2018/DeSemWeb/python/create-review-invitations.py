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
import sys
import os
from openreview import *
from openreview import tools

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "Connecting to "+client.baseurl

CONFERENCE_ID = 'swsa.semanticweb.org/ISWC/2018/DeSemWeb'
PROGRAM_CHAIRS = CONFERENCE_ID+'/ProgramChairs'

# TODO get real info 5/15/18 11:59 pm Hawaii time = 5/16/18 9:59am GMT
REVIEW_TIMESTAMP =  tools.timestamp_GMT(2018,6,16,10)

review_params = {
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'process': os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js'),
    'duedate': REVIEW_TIMESTAMP
}

review_content = {
    'title': {
        'order': 1,
        'value-regex': '.{0,500}',
        'description': 'Brief summary of your review (up to 500 chars).',
        'required': True
    },
    'review': {
        'order': 2,
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (up to 5000 chars).',
        'required': True
    },
    'rating': {
        'order': 3,
        'value-dropdown': [
            '-3',
            '-2',
            '-1',
            '0',
            '1',
            '2',
            '3'
        ],
        'required': True
    }
}

tools.post_submission_groups(client, CONFERENCE_ID, CONFERENCE_ID+'/-/Submission', PROGRAM_CHAIRS)
submissions = client.get_notes(invitation=CONFERENCE_ID+'/-/Submission')
for paper in submissions:
    paper_num = str(paper.number)
    paperinv = CONFERENCE_ID + '/-/Paper' + paper_num
    paperGroup = CONFERENCE_ID + '/Paper' + paper_num
    ## review invitation
    review_reply = {
        'forum':paper.id,
        'replyto':paper.id,
        'writers':{'values-regex': '~.*|'+paperGroup + '/AnonReviewer[0-9]+'},
        "signatures": {
            "values-regex": '~.*|'+paperGroup + '/AnonReviewer[0-9]+',
            "description": "How your identity will be displayed with the above content."
        },
        'readers':{
            'values': ['everyone'],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': review_content
    }
    invite = openreview.Invitation(paperinv + '/Official/Review',**review_params)
    invite.reply= review_reply
    invite.invitees = [paperGroup + '/Reviewers']
    invite.noninvitees = []

    client.post_invitation(invite)
