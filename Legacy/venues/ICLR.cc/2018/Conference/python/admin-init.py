#!/usr/bin/python

import sys, os
import argparse
import openreview
import config

"""

OPTIONAL SCRIPT ARGUMENTS

	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password

"""

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

groups = {}
groups[config.PROGRAM_CHAIRS] = openreview.Group(config.PROGRAM_CHAIRS, **config.program_chairs_params)

groups[config.AUTHORS] = openreview.Group(config.AUTHORS, **config.group_params)

groups[config.AREA_CHAIRS] = openreview.Group(config.AREA_CHAIRS, **config.area_chairs_params)
groups[config.AREA_CHAIRS_INVITED] = openreview.Group(config.AREA_CHAIRS_INVITED, **config.group_params)
groups[config.AREA_CHAIRS_DECLINED] = openreview.Group(config.AREA_CHAIRS_DECLINED, **config.group_params)
groups[config.AREA_CHAIRS_EMAILED] = openreview.Group(config.AREA_CHAIRS_EMAILED, **config.group_params)

groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.reviewer_group_params)
groups[config.REVIEWERS_INVITED] = openreview.Group(config.REVIEWERS_INVITED, **config.reviewer_group_params)
groups[config.REVIEWERS_DECLINED] = openreview.Group(config.REVIEWERS_DECLINED, **config.reviewer_group_params)
groups[config.REVIEWERS_EMAILED] = openreview.Group(config.REVIEWERS_EMAILED, **config.reviewer_group_params)

groups[config.AUTHORS_PLUS] = openreview.Group(config.AUTHORS_PLUS, members = [config.AUTHORS, config.REVIEWERS_PLUS], **config.public_group_params)
groups[config.REVIEWERS_PLUS] = openreview.Group(config.REVIEWERS_PLUS, members = [config.CONF, config.REVIEWERS, config.AREA_CHAIRS, config.PROGRAM_CHAIRS], **config.public_group_params)
groups[config.AREA_CHAIRS_PLUS] = openreview.Group(config.AREA_CHAIRS_PLUS, members = [config.CONF, config.AREA_CHAIRS, config.PROGRAM_CHAIRS], **config.public_group_params)

groups[config.CONF] = client.get_group(config.CONF)
groups[config.CONF].signatures = [client.signature]
groups[config.CONF].add_webfield(config.WEBPATH)

invitations = {}
invitations[config.SUBMISSION] = openreview.Invitation(
	config.SUBMISSION, duedate=config.DUE_TIMESTAMP, **config.submission_params)

invitations[config.BLIND_SUBMISSION] = openreview.Invitation(
	config.BLIND_SUBMISSION, **config.blind_submission_params)

invitations[config.WITHDRAWN_SUBMISSION] = openreview.Invitation(
	config.WITHDRAWN_SUBMISSION, **config.withdrawn_submission_params)

invitations[config.PUBLIC_COMMENT] = openreview.Invitation(
	config.PUBLIC_COMMENT, **config.public_comment_params)

invitations[config.ADD_BID] = openreview.Invitation(
	config.ADD_BID, **config.add_bid_params)

invitations[config.METADATA] = openreview.Invitation(
	config.METADATA, **config.metadata_params)

invitations[config.ASSIGNMENTS] = openreview.Invitation(
	config.ASSIGNMENTS, **config.assignments_params)

invitations[config.RECRUIT_AREA_CHAIRS] = openreview.Invitation(
	config.RECRUIT_AREA_CHAIRS, **config.recruit_area_chairs_params)

invitations[config.RECRUIT_REVIEWERS] = openreview.Invitation(
	config.RECRUIT_REVIEWERS, **config.recruit_reviewers_params)

for g in groups.values():
	print "Posting group: ", g.id
	client.post_group(g)

for i in invitations.values():
	print "Posting invitation: ", i.id
	client.post_invitation(i)
