#!/usr/bin/python

###############################################################################
# ex. python create-invitations.py --baseurl http://localhost:3000
#       --username admin --password admin_pw  --track Poster
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
import rssdata

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--track', help="'Poster' or 'Proceedings'")

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)


## check review process function exists
review_path = "../process/officialReview{0}Process.js".format(args.track)
if os.path.isfile(review_path) is False:
    print "Cannot locate review process function at:"+review_path
    sys.exit()

conf_track = rssdata.CONFERENCE+'/-_'+args.track
submissions = client.get_notes(invitation=conf_track+'/-/Submission')
print conf_track+'/-/Submission'
review_content = {
    'title': {
        'order': 1,
        'value-regex': '.{0,500}',
        'description': 'Brief summary of your review.',
        'required': True
    },
    'review': {
        'order': 2,
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
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

for paper in submissions:
    paper_num = str(paper.number)
    paperinv = conf_track + '/-/Paper' + paper_num;
    print("Adding groups for Paper"+ paper_num)

    ## Paper Group
    paperGroup = conf_track + '/Paper' + paper_num;
    client.post_group(openreview.Group(
        id=paperGroup,
        signatures=[conf_track],
        writers=[conf_track],
        members=[],
        readers=['everyone'],
        signatories=[]))

    ## Author group
    authorGroup = paperGroup + '/Authors'
    client.post_group(openreview.Group(
        id=authorGroup,
        signatures=[conf_track],
        writers=[conf_track],
        members=[],
        readers=[conf_track, rssdata.COCHAIRS, authorGroup],
        signatories=[]))

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    client.post_group(openreview.Group(
        id=reviewerGroup,
        signatures=[conf_track],
        writers=[conf_track],
        members=[],
        readers=[conf_track, rssdata.COCHAIRS, reviewerGroup],
        signatories=[]))

    ## NonReviewers - people that aren't allowed to see the reviews.
    # Used to prevent reviewers from seeing other reviews of that paper
    # until their review is complete.
    nonReviewerGroup = reviewerGroup + '/NonReaders'
    client.post_group(openreview.Group(
        id=nonReviewerGroup,
        signatures=[conf_track],
        writers=[conf_track],
        members=[],
        readers=[conf_track, rssdata.COCHAIRS],
        signatories=[]))

    ## review invitation
    review_reply = {
        'forum':paper.id,
        'replyto':paper.id,
        'writers':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'signatures':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'readers':{
            'values': [rssdata.COCHAIRS, authorGroup],
            'description': 'The users who will be allowed to read the above content.'
        },
        'nonreaders':{
            'values': [nonReviewerGroup]},
        'content':review_content
    }
    client.post_invitation(openreview.Invitation(paperinv + '/Official/Review',
                                                 signatures=[conf_track],
                                                 writers=[conf_track],
                                                 invitees=[paperGroup + '/Reviewers'],
                                                 noninvitees=[],
                                                 readers=[rssdata.COCHAIRS, reviewerGroup],
                                                 process=review_path,
                                                 duedate=rssdata.REVIEW_DUE,
                                                 reply=review_reply))