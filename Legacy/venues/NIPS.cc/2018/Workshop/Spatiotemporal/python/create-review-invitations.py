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

    if paper.number > 32:
        ## Reviewer group - people that can see the review invitation
        reviewerGroup = paperGroup + '/Reviewers'
        try:
            client.get_group(id=reviewerGroup)
            print("Found " + reviewerGroup)
        except openreview.OpenReviewException as e:
            # is group not found, then make groups and invites
            print(e.args[0][0])
            if e.args[0][0].startswith('Group Not Found'):
                client.post_group(openreview.Group(
                    id=reviewerGroup,
                    signatures=[config.CONFERENCE_ID],
                    writers=[config.CONFERENCE_ID],
                    members=[],
                    readers=[config.CONFERENCE_ID, config.PROGRAM_CHAIRS],
                    signatories=[]))


        ## Confidential Review
        review_reply = {
            'forum': paper.id,
            'replyto': paper.id,
            'writers': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
            'signatures': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
            'readers': {
                'values': [config.CONFERENCE_ID, config.PROGRAM_CHAIRS],
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {
                'relevance': {
                    'order': 1,
                    'description': 'Relevance to the workshop',
                    'value-radio': [
                        '5: very high',
                        '4: high',
                        '3: borderline',
                        '2: low',
                        '1: very low'
                    ],
                    'required': True
                },
                'novelty': {
                    'order': 2,
                    'value-radio': [
                        '5: very high',
                        '4: high',
                        '3: borderline',
                        '2: low',
                        '1: very low'
                    ],
                    'required': True
                },
                'impact': {
                    'order': 3,
                    'description': 'Potential impact',
                    'value-radio': [
                        '5: very high',
                        '4: high',
                        '3: borderline',
                        '2: low',
                        '1: very low'
                    ],
                    'required': True
                }
            }
        }

        review_parameters = config.review_params
        review_parameters['reply'] = review_reply
        review_parameters['invitees'] = [paperGroup + '/Reviewers']
        invite = openreview.Invitation(paperinv + '/Confidential_Review', **review_parameters)
        client.post_invitation(invite)

        ## Overall Evaluation
        eval_parameters = {
            'readers': ['everyone'],
            'writers': [config.CONFERENCE_ID],
            'invitees': [paperGroup + '/Reviewers'],
            'signatures': [config.CONFERENCE_ID],
            'process': os.path.join(os.path.dirname(__file__), '../process/overallEvaluationProcess.js'),
            'duedate': config.REVIEW_TIMESTAMP
        }
        eval_parameters['reply'] = {
            'forum': paper.id,
            'replyto': paper.id,
            'writers': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
            'signatures': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
            'readers': {
                'values': [config.CONFERENCE_ID, config.PROGRAM_CHAIRS, paperGroup + '/Authors'],
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {'evaluation': {
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Text up to 5000 chars. Currently visible to Authors and Program Chairs, will become public.',
                'required': True
            }},
        }
        invite = openreview.Invitation(paperinv + '/Overall_Evaluation', **eval_parameters)
        client.post_invitation(invite)


        ## Official Comment
        comment_parameters = {
            'readers': ['everyone'],
            'writers': [config.CONFERENCE_ID],
            'invitees': [config.PROGRAM_CHAIRS, paperGroup + '/Reviewers'],
            'signatures': [config.CONFERENCE_ID],
            'process': os.path.join(os.path.dirname(__file__), '../process/officialCommentProcess.js')
        }
        comment_parameters['reply'] = {
            'forum': paper.id,
            'replyto': None,
            'writers': {'values-regex': config.PROGRAM_CHAIRS+'|'+paperGroup + '/AnonReviewer[0-9]+'},
            'signatures': {'values-regex': config.PROGRAM_CHAIRS+'|'+paperGroup + '/AnonReviewer[0-9]+'},
            'readers': {
                'values': [config.CONFERENCE_ID, config.PROGRAM_CHAIRS, paperGroup + '/Reviewers'],
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {'comment': {
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Further comments (if any): only visible to the program chair. Text up to 5000 chars.',
                'required': True
            }}
        }
        invite = openreview.Invitation(paperinv + '/Official_Comment', **comment_parameters)
        client.post_invitation(invite)
