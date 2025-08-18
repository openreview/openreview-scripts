#!/usr/bin/python


import argparse
import openreview
from openreview import tools
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

conference.close_submissions()
conference.set_authors()

print('replacing members with IDs')
reviewers_group = client.get_group(conference.get_reviewers_id())
openreview.tools.replace_members_with_ids(client, reviewers_group)

conference.create_blind_submissions()