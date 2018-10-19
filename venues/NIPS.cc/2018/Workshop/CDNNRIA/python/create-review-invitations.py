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

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    try:
        client.get_group(id=reviewerGroup)
        print("Found "+reviewerGroup)
    except openreview.OpenReviewException as e:
        # is group not found, then make groups and invites
        print(e.args[0][0])
        if e.args[0][0].startswith('Group Not Found'):
            print("Create "+reviewerGroup)
            client.post_group(openreview.Group(
                id=reviewerGroup,
                signatures=[config.CONFERENCE_ID],
                writers=[config.CONFERENCE_ID],
                members=[],
                readers=[config.CONFERENCE_ID, config.PROGRAM_CHAIRS],
                signatories=[]))

            ## Review
            review_reply = {
                'forum': paper.id,
                'replyto': paper.id,
                'writers': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
                'signatures': {'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
                'readers': {
                    'values': ['everyone'],
                    'description': 'The users who will be allowed to read the above content.'
                },
                'content':  {
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
                        'order': 4,
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
                        'order': 5,
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
                'writers': [config.CONFERENCE_ID],
                'signatures': [config.CONFERENCE_ID],
                'process': os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js'),
                'duedate': config.REVIEW_TIMESTAMP,
                'reply': review_reply,
                'invitees': [paperGroup + '/Reviewers']
            }
            invite = openreview.Invitation(paperinv + '/Official_Review', **review_parameters)
            client.post_invitation(invite)


            ## Official Comment
            comment_parameters = {
                'readers': ['everyone'],
                'writers': [config.CONFERENCE_ID],
                'invitees': [config.PROGRAM_CHAIRS, config.REVIEWERS, reviewerGroup, authorGroup],
                'signatures': [config.CONFERENCE_ID],
                'process': os.path.join(os.path.dirname(__file__), '../process/officialCommentProcess.js')
            }
            comment_parameters['reply'] = {
                'forum': paper.id,
                'replyto': None,
                'writers': {'values-regex': config.PROGRAM_CHAIRS+'|'+config.REVIEWERS+'|'+paperGroup + '/AnonReviewer[0-9]+|'+authorGroup},
                'signatures': {'values-regex': config.PROGRAM_CHAIRS+'|'+config.REVIEWERS+'|'+paperGroup + '/AnonReviewer[0-9]+|'+authorGroup},
                'readers': {
                    'values': ['everyone'],
                    'description': 'The users who will be allowed to read the above content.'
                },
                'content': {'comment': {
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Official comments: Reviewers and authors remain anonymous to everyone except the PCS. Text up to 5000 chars.',
                    'required': True
                }}
            }
            invite = openreview.Invitation(paperinv + '/Official_Comment', **comment_parameters)
            client.post_invitation(invite)
