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

iterator = tools.iterget_notes(client, invitation=conference.get_submission_id())
for paper in iterator:
    paper_num = str(paper.number)
    paperinv = conference.get_id() + '/-/Paper' + paper_num + '/Meta_Review'
    paperGroup = conference.get_id() + '/Paper' + paper_num

    ## Confidential Review
    metareview_reply = {
        'forum': paper.id,
        'replyto': paper.id,
        'writers': {'values-regex': paperGroup + '/Area_Chair[0-9]+'},
        'signatures': {'values-regex': paperGroup + '/Area_Chair[0-9]+'},
        'readers': {
            'values': [conference.get_id(), conference.get_program_chairs_id(), paperGroup + '/Area_Chairs'],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': {
            'title': {
                'order': 1,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your review.',
                'required': True
            },
            'metareview': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
                'required': True
            },
            'recommendation': {
                'order': 3,
                'value-radio': [
                    'Accept (Oral)',
                    'Accept (Poster)',
                    'Reject'
                ],
                'required': True
            },
            'confidence': {
                'order': 4,
                'value-radio': [
                    '3: The area chair is absolutely certain',
                    '2: The area chair is fairly confident',
                    '1: The area chair\'s evaluation is an educated guess'
                ],
                'required': True
            }
        }
    }

    metareview_parameters = {
        'readers': ['everyone'],
        'writers': [conference.get_id()],
        'signatures': [conference.get_id()],
        'duedate': tools.timestamp_GMT(2019, month=2, day= 17, hour=23, minute=59),
        'invitees': [paperGroup + '/Area_Chairs'],
        'reply': metareview_reply
    }

    invite = openreview.Invitation(paperinv, **metareview_parameters)
    client.post_invitation(invite)
    print(invite.id)


