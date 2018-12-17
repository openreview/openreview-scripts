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
conference.set_authors()

iterator = tools.iterget_notes(client, invitation=conference.get_submission_id())
for paper in iterator:
    paper_num = str(paper.number)
    paperinv = conference.get_id() + '/-/Paper' + paper_num + '/Official_Review'
    paperGroup = conference.get_id() + '/Paper' + paper_num

    ## Confidential Review
    review_reply = {
        'forum': paper.id,
        'replyto': paper.id,
        'writers': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'signatures': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'readers': {
            'values': [conference.get_id(), conference.get_program_chairs_id(), paperGroup + '/Area_Chairs'],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': {
            'review': {
                'order': 1,
                'value-regex': '[\\S\\s]{1,500000}',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons. Remember that MIDL values both methodological contributions and application articles that present solid validation.',
                'required': True
            },
            'rating': {
                'order': 2,
                'value-radio': [
                    '4: strong accept',
                    '3: accept',
                    '2: reject',
                    '1: strong reject'
                ],
                'required': True
            },
            'confidence': {
                'order': 3,
                'value-radio': [
                    '3: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
                    '2: The reviewer is fairly confident that the evaluation is correct',
                    '1: The reviewer\'s evaluation is an educated guess'
                ],
                'required': True
            },
            'special_issue': {
                'order': 4,
                'value-checkbox': ['Special Issue Recommendation'],
                'required': False
            },
            'oral_presentation': {
                'order': 5,
                'value-checkbox': ['Consider for oral presentation'],
                'required': False
            }
        }
    }

    review_parameters = {
        'readers': ['everyone'],
        'writers': [conference.get_id()],
        'signatures': [conference.get_id()],
        'duedate': tools.timestamp_GMT(2019, month=1, day= 29, hour=8, minute=0)
    }
    review_parameters['reply'] = review_reply
    review_parameters['invitees'] = [paperGroup + '/Reviewers']
    invite = openreview.Invitation(paperinv, **review_parameters)
    client.post_invitation(invite)
    print(invite.id)


