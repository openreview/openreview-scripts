#!/usr/bin/python

###############################################################################
# ex. python create-invitations.py --cpath MyConf.org/2017 --baseurl http://localhost:3000
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

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--cpath', required=True, help="conference path ex. MyConf.org/2017")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

## check conference directory exists
base_path = "../../venues/"+args.cpath
config_path = base_path+"/python/"
if os.path.isfile(config_path+"config.py") is False:
    print "Cannot locate config.py in:"+config_path
    sys.exit()
## load conference specific data
sys.path.insert(0, config_path)
import config

## check review process function exists
review_path = base_path+'/process/officialReviewProcess.js'
if os.path.isfile(review_path) is False:
    print "Cannot locate review process function at:"+review_path
    sys.exit()

submissions = client.get_notes(invitation=config.SUBMISSION)
for paper in submissions:
    paper_num = str(paper.number)
    paperinv = config.CONF + '/-/Paper' + paper_num;
    print("Adding groups for Paper"+ paper_num)

    ## Paper Group
    paperGroup = config.CONF + '/Paper' + paper_num;
    client.post_group(openreview.Group(
        id=paperGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=['everyone'],
        signatories=[]))

    ## Author group
    authorGroup = paperGroup + '/Authors'
    client.post_group(openreview.Group(
        id=authorGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[paper.content['authorids']],
        readers=[config.CONF, config.PROGRAM_CHAIRS, authorGroup],
        signatories=[]))

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    client.post_group(openreview.Group(
        id=reviewerGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, reviewerGroup],
        signatories=[]))

    ## NonReviewers - people that aren't allowed to see the reviews.
    # Used to prevent reviewers from seeing other reviews of that paper
    # until their review is complete.
    nonReviewerGroup = reviewerGroup + '/NonReaders'
    client.post_group(openreview.Group(
        id=nonReviewerGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS],
        signatories=[]))

    ## review invitation
    review_reply = {
        'forum':paper.id,
        'replyto':paper.id,
        'writers':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'signatures':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'readers':{
            'values': [config.CONF, config.PROGRAM_CHAIRS, reviewerGroup, authorGroup],
            'description': 'The users who will be allowed to read the above content.'
        },
        'nonreaders':{
            'values': [nonReviewerGroup]},
        'content':config.review_content
    }
    client.post_invitation(openreview.Invitation(paperinv + '/Official/Review',
                                                 signatures=[config.CONF],
                                                 writers=[config.CONF],
                                                 invitees=[paperGroup + '/Reviewers'],
                                                 noninvitees=[],
                                                 readers=['everyone'],
                                                 process=review_path,
                                                 duedate=config.REVIEW_DUE,
                                                 reply=review_reply))