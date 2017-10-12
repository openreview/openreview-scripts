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
groups[config.AREA_CHAIRS] = openreview.Group(config.AREA_CHAIRS, **config.group_params)
groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.group_params)

groups[config.CONFERENCE_ID] = client.get_group(config.CONFERENCE_ID)
groups[config.CONFERENCE_ID].signatures = [client.signature]
groups[config.CONFERENCE_ID].add_webfield(config.WEBPATH)

invitations = {}
invitations[config.SUBMISSION] = openreview.Invitation(config.SUBMISSION, duedate=config.SUBMISSION_TIMESTAMP, **config.submission_params)
invitations[config.COMMENT] = openreview.Invitation(config.COMMENT, **config.comment_params)

invitations[config.SUBMISSION].reply = config.submission_reply
invitations[config.COMMENT].reply = config.comment_reply

for g in groups.values():
	print "Posting group: ", g.id
	client.post_group(g)

for i in invitations.values():
	print "Posting invitation: ", i.id
	client.post_invitation(i)
