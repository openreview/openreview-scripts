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

# add the workshop group as a member of the conference group so that it can access the "invited to workshop" papers
client.add_members_to_group(client.get_group('ICLR.cc/2018/Conference'), 'ICLR.cc/2018/Workshop')

conference = client.post_group(
	openreview.Group(
		config.CONF,
		web = config.WEBPATH,
		signatures = [client.signature],
		readers = ['everyone'],
		writers = [config.CONF],
		signatories = [config.CONF]
	))

program_chairs = client.post_group(
	openreview.Group(**config.program_chairs_params))

authors = client.post_group(
	openreview.Group(config.AUTHORS, **config.group_params))

reviewers = client.post_group(
	openreview.Group(config.REVIEWERS, **config.reviewer_group_params))

reviewers_invited = client.post_group(
	openreview.Group(config.REVIEWERS_INVITED, **config.reviewer_group_params))

reviewers_declined = client.post_group(
	openreview.Group(config.REVIEWERS_DECLINED, **config.reviewer_group_params))

reviewers_emailed = client.post_group(
	openreview.Group(config.REVIEWERS_EMAILED, **config.reviewer_group_params))

authors_plus = client.post_group(
	openreview.Group(
		config.AUTHORS_PLUS,
		members = [config.AUTHORS, config.REVIEWERS_PLUS],
		**config.public_group_params))

reviewers_plus = client.post_group(
	openreview.Group(
		config.REVIEWERS_PLUS,
		members = [config.CONF, config.REVIEWERS, config.PROGRAM_CHAIRS],
		**config.public_group_params))

submission_invitation = client.post_invitation(
	openreview.Invitation(
		config.SUBMISSION,
		duedate=config.DUE_TIMESTAMP,
		**config.submission_params))

transfer_invitation = client.post_invitation(
    openreview.Invitation(
        config.TRANSFER_FROM_CONFERENCE,
        duedate=config.DUE_TIMESTAMP,
        **config.transfer_from_conference_params))

withdrawn_submission = client.post_invitation(
	openreview.Invitation(
		config.WITHDRAWN_SUBMISSION,
		**config.withdrawn_submission_params))

public_comment_invitation = client.post_invitation(
	openreview.Invitation(
		config.PUBLIC_COMMENT,
		**config.public_comment_params))

add_bid_invitation = client.post_invitation(
	openreview.Invitation(
		config.ADD_BID,
		**config.add_bid_params))

metadata_invitation = client.post_invitation(
	openreview.Invitation(
		config.METADATA,
		**config.metadata_params))

assignments_invitation = client.post_invitation(
	openreview.Invitation(
		config.ASSIGNMENTS,
		**config.assignments_params))

recruit_reviewers_invitation = client.post_invitation(
	openreview.Invitation(
		config.RECRUIT_REVIEWERS,
		**config.recruit_reviewers_params))
