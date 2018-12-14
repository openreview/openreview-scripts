#!/usr/bin/python

import sys, os
import argparse
import datetime
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
print('connecting to {0}'.format(client.baseurl))

conference = config.get_conference(client)

print('open comment invitations')
conference.set_authors()
conference.open_comments(name = 'Official_Comment', public = False, anonymous = True)

print('replacing members with IDs')
reviewers_group = client.get_group(conference.get_reviewers_id())
areachairs_group = client.get_group(conference.get_area_chairs_id())
openreview.tools.replace_members_with_ids(client, reviewers_group)
openreview.tools.replace_members_with_ids(client, areachairs_group)
