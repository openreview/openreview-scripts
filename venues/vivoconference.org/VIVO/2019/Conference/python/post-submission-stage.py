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

print('open public comment invitations')
# conference.open_comments(name = 'Official_Comment', public = False, anonymous = True)
conference.open_comments(name = 'Public_Comment', public = False, anonymous = True)
public_comments = openreview.tools.iterget_invitations(client, regex='vivoconference.org/VIVO/2019/Conference/-/Paper.*/Public_Comment$')
for comment_invi in public_comments:
	comment_id = comment_invi.id
	paper_number = comment_id.split('Paper')[1].split('/')[0]
	comment_invi.invitees = ['~']

	readers = comment_invi.reply['readers']['values-dropdown']
	readers = [
		'everyone',
		'vivoconference.org/VIVO/2019/Conference/Paper' + str(paper_number) + '/Authors',
		'vivoconference.org/VIVO/2019/Conference/Paper' + str(paper_number) + '/Reviewers',
		"vivoconference.org/VIVO/2019/Conference/Program_Chairs"]
	comment_invi.reply['readers']['values-dropdown'] = readers

	sign = comment_invi.reply['signatures']['values-regex'] + '|~.*|\\(anonymous\\)'
	comment_invi.reply['signatures']['values-regex'] = sign
	client.post_invitation(comment_invi)

print('replacing members with IDs')
reviewers_group = client.get_group(conference.get_reviewers_id())
openreview.tools.replace_members_with_ids(client, reviewers_group)

