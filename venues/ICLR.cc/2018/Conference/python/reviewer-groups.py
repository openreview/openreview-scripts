#!/usr/bin/python

###############################################################################
# ex. python reviewer-groups.py --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# To be run after submission due date to create review invitations for all the papers.
# For each paper:
# 1) create reviewer group (reviewers for this paper)
#           and nonReviewerGroup (folks that aren't allowed to read the review at least not yet)
# 2) create review invitation
###############################################################################

## Import statements
import argparse
import sys
import config
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
for paper in submissions:
    paper_num = str(paper.number)
    paperinv = config.CONF + '/-/Paper' + paper_num
    print("Adding groups for Paper"+ paper_num)
    paperGroup = config.CONF + '/Paper' + paper_num
    authorGroup = paperGroup + '/Authors'

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    client.post_group(openreview.Group(
        id=reviewerGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS],
        signatories=[]))

    anonReviewer1GroupId = paperGroup + '/AnonReviewer1'
    client.post_group(openreview.Group(
        id=anonReviewer1GroupId,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, anonReviewer1GroupId],
        nonreaders=[authorGroup],
        signatories=[anonReviewer1GroupId]))

    anonReviewer2GroupId = paperGroup + '/AnonReviewer2'
    client.post_group(openreview.Group(
        id=anonReviewer2GroupId,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, anonReviewer2GroupId],
        nonreaders=[authorGroup],
        signatories=[anonReviewer2GroupId]))

    anonReviewer3GroupId = paperGroup + '/AnonReviewer3'
    client.post_group(openreview.Group(
        id=anonReviewer3GroupId,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, anonReviewer3GroupId],
        nonreaders=[authorGroup],
        signatories=[anonReviewer3GroupId]))

    anonReviewer4GroupId = paperGroup + '/AnonReviewer4'
    client.post_group(openreview.Group(
        id=anonReviewer4GroupId,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, anonReviewer4GroupId],
        nonreaders=[authorGroup],
        signatories=[anonReviewer4GroupId]))

    anonReviewer5GroupId = paperGroup + '/AnonReviewer5'
    client.post_group(openreview.Group(
        id=anonReviewer5GroupId,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, anonReviewer5GroupId],
        nonreaders=[authorGroup],
        signatories=[anonReviewer5GroupId]))

    ## Area Chair group -
    areachairGroup = paperGroup + '/Area_Chair'
    client.post_group(openreview.Group(
        id=areachairGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, areachairGroup],
        signatories=[areachairGroup]))

    ## update invitations with area chair and reviewer groups
    public_comment_inv = client.get_invitation(paperinv+'/Public_Comment')
    public_comment_inv.noninvitees = [authorGroup, reviewerGroup, areachairGroup]
    client.post_invitation(public_comment_inv)

    official_comment_inv = client.get_invitation(paperinv + '/Official_Comment')
    official_comment_inv.invitees =  [authorGroup, reviewerGroup, areachairGroup, config.PROGRAM_CHAIRS]
    official_comment_inv.reply['signatures']['values-regex'] = '{}|{}|{}|{}'.format(paperGroup+'/AnonReviewer[0-9]+', authorGroup, areachairGroup, config.PROGRAM_CHAIRS)
    official_comment_inv.reply['writers']['values-regex'] = '{}|{}|{}|{}'.format(paperGroup+'/AnonReviewer[0-9]+', authorGroup, areachairGroup, config.PROGRAM_CHAIRS)
    client.post_invitation(official_comment_inv)

