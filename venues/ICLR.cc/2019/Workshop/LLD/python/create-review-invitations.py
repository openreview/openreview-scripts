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
import openreview
from openreview import tools
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)

conference = config.get_conference(client)

notes = conference.get_submissions()
for paper in notes:
    paper_num = str(paper.number)
    paperinv = conference.get_id() + '/-/Paper' + paper_num + '/Official_Review'
    paperGroup = conference.get_id() + '/Paper' + paper_num

    ## Confidential Review
    review_reply = {
        'forum': paper.id,
        'replyto': paper.id,
        'writers': {'description': 'How your identity will be displayed.',
                    'values-regex': paperGroup + '/AnonReviewer[0-9]+|~.*'},
        'signatures': {'values-regex': paperGroup + '/AnonReviewer[0-9]+|~.*'},
        'readers': {
            'values': [conference.get_program_chairs_id()],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': {
            'title': {
                'order': 1,
                'value-regex': '.{0,500}',
                'description': 'Brief summary of your review.',
                'required': True
            },
            'review': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,200000}',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (max 200000 characters).',
                'required': True
            },
            'rating': {
                'order': 3,
                'value-dropdown': [
                    '5: Top 15% of accepted papers, strong accept',
                    '4: Top 50% of accepted papers, clear accept',
                    '3: Marginally above acceptance threshold',
                    '2: Marginally below acceptance threshold',
                    '1: Strong rejection'
                ],
                'required': True
            },
            'confidence': {
                'order': 4,
                'value-radio': [
                    '3: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
                    '2: The reviewer is fairly confident that the evaluation is correct',
                    '1: The reviewer\'s evaluation is an educated guess'
                ],
                'required': True
            }
        }
    }

    review_parameters = {
        'readers': ['everyone'],
        'writers': [conference.get_id()],
        'signatures': [conference.get_id()],
        # The deadline for the reviews is the April 7th.
        'duedate': tools.timestamp_GMT(2019, month=4, day= 8, hour=0, minute=0),
        'expdate': tools.timestamp_GMT(2019, month=4, day=15, hour=0, minute=0),
        'reply': review_reply,
        'invitees': [paperGroup + '/Reviewers']
    }

    invite = openreview.Invitation(paperinv, **review_parameters)
    client.post_invitation(invite)
    print(invite.id)


