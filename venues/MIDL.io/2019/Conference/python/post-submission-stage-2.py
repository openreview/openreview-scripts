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

print('make reviews visible to reviewers and authors of the paper')
invitations = tools.iterget_invitations(client, regex=conference.get_id() + '/-/Paper.*/Official_Review')
for invite in invitations:
    paper_num = invite.id.split('/Paper')[1].split('/')[0]
    invite.reply['readers']['values'].extend([conference.get_id() + '/Paper' + paper_num + '/Reviewers',
                                              conference.get_id() + '/Paper' + paper_num + '/Authors'])
    client.post_invitation(invite)

reviews = tools.iterget_notes(client, invitation=conference.get_id() + '/-/Paper.*/Official_Review')
for review in reviews:
    paper_num = review.invitation.split('/Paper')[1].split('/')[0]
    review.readers.extend([conference.get_id() + '/Paper' + paper_num + '/Reviewers',
                           conference.get_id() + '/Paper' + paper_num + '/Authors'])
    client.post_note(review)

print('open comment invitations')
conference.set_authors()
conference.open_comments(name = 'Official_Comment', public = False, anonymous = True)

print('replacing members with IDs')
reviewers_group = client.get_group(conference.get_reviewers_id())
areachairs_group = client.get_group(conference.get_area_chairs_id())
openreview.tools.replace_members_with_ids(client, reviewers_group)
openreview.tools.replace_members_with_ids(client, areachairs_group)
