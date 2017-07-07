#!/usr/bin/python

import openreview
import sys, os
import config
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

"""

OPTIONAL SCRIPT ARGUMENTS

	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password

"""

subprocess.call([
    "node",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../utils/processToFile.js")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../process/submissionProcess.template")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../process"))
])

groups = {}
prog_chairs = openreview.Group(config.PROGRAM_CHAIRS, **config.group_params)
prog_chairs.members = [] # don't commit real member identities
groups[config.PROGRAM_CHAIRS] = prog_chairs
groups[config.AREA_CHAIRS] = openreview.Group(config.AREA_CHAIRS, **config.group_params)
groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.group_params)

invitations = {}
invitations[config.SUBMISSION] = openreview.Invitation(config.SUBMISSION, duedate=config.DUE_TIMESTAMP, **config.submission_params)
invitations[config.COMMENT] = openreview.Invitation(config.COMMENT, **config.comment_params)

invitations[config.SUBMISSION].reply = config.submission_reply
invitations[config.COMMENT].reply = config.comment_reply


for g in groups.values():
	print "Posting group: ", g.id
	client.post_group(g)

for i in invitations.values():
	print "Posting invitation: ", i.id
	client.post_invitation(i)
