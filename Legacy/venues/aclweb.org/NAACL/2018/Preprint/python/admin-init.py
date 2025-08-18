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

groups = []

naacl_groups = openreview.tools.build_groups(config.CONF)
groups += naacl_groups

groups.append(openreview.Group(config.AUTHORS, **config.group_params))

conf_group = [n for n in naacl_groups if n.id == config.CONF][0]
conf_group.signatures = [client.signature]
conf_group.add_webfield(config.WEBPATH)

invitations = []
invitations.append(openreview.Invitation(
    config.SUBMISSION, duedate=config.DUE_TIMESTAMP, **config.submission_params))

invitations.append(openreview.Invitation(
    config.BLIND_SUBMISSION, **config.blind_submission_params))

# public comments are disabled for now

for g in groups:
    print "Posting group: ", g.id
    client.post_group(g)

for i in invitations:
    print "Posting invitation: ", i.id
    client.post_invitation(i)
