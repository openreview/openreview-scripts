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

#TODO need real date
# using June 2 noon GMT or June1 midnight AoE
REVIEW_DUEDATE = tools.timestamp_GMT(2018, 6, 2, 12)
CONFERENCE_ID = 'IEEE.org/2018/ITSC'
PROGRAM_CHAIRS = 'IEEE.org/2018/ITSC/Program_Chairs'
submissions = client.get_notes(invitation='IEEE.org/2018/ITSC/-/Submission')
blind_submissions = client.get_notes(invitation='IEEE.org/2018/ITSC/-/Blind_Submission')
for paper in submissions:
    paper_num = str(paper.number)
    paperinv = CONFERENCE_ID + '/-/Paper' + paper_num
    print("Adding groups for Paper"+ paper_num)

    ## Paper Group
    paperGroup = CONFERENCE_ID + '/Paper' + paper_num
    client.post_group(openreview.Group(
        id=paperGroup,
        signatures=[CONFERENCE_ID],
        writers=[CONFERENCE_ID],
        members=[],
        readers=['everyone'],
        signatories=[]))

    ## Author group
    authorGroup = paperGroup + '/Authors'
    client.post_group(openreview.Group(
        id=authorGroup,
        signatures=[CONFERENCE_ID],
        writers=[CONFERENCE_ID],
        members=paper.content['authorids'],
        readers=[CONFERENCE_ID, PROGRAM_CHAIRS, authorGroup],
        signatories=[]))

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    client.post_group(openreview.Group(
        id=reviewerGroup,
        signatures=[CONFERENCE_ID],
        writers=[CONFERENCE_ID],
        members=[],
        readers=[CONFERENCE_ID, PROGRAM_CHAIRS],
        signatories=[]))

    ## NonReviewers - people that aren't allowed to see the reviews.
    # Used to prevent reviewers from seeing other reviews of that paper
    # until their review is complete.
    nonReviewerGroup = reviewerGroup + '/NonReaders'
    client.post_group(openreview.Group(
        id=nonReviewerGroup,
        signatures=[CONFERENCE_ID],
        writers=[CONFERENCE_ID],
        members=[],
        readers=[CONFERENCE_ID, PROGRAM_CHAIRS],
        signatories=[]))

    ## review invitation
    blind_note = next((item for item in blind_submissions if item.number == paper.number), None)
    review_reply = {
        'forum':blind_note.id,
        'replyto':blind_note.id,
        'writers':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'signatures':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'readers':{
            'values': [CONFERENCE_ID, PROGRAM_CHAIRS, reviewerGroup, authorGroup],
            'description': 'The users who will be allowed to read the above content.'
        },
        'nonreaders':{
            'values': [nonReviewerGroup]},
        'content': {
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
    invite = openreview.Invitation(paperinv + '/Official/Review',
                                    readers = ['everyone'],
                                    writers=[CONFERENCE_ID],
                                    signatures= [CONFERENCE_ID],
                                    reply= review_reply,
                                    invitees = [paperGroup + '/Reviewers'],
                                    noninvitees = [],
                                    process= os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js'),
                                    duedate = REVIEW_DUEDATE
    )
    client.post_invitation(invite)
