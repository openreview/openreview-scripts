#!/usr/bin/python

import argparse
import openreview
from openreview import tools
from openreview import invitations
import config
import datetime

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
conference.open_submissions(due_date = datetime.datetime(2019, 4, 16, 12, 00), additional_fields = {
    "author_identity_visibility": {
        "order": 4,
        "value-checkbox": "Reveal author identities to reviewers",
        "required": False
    }
})

# doesn't seem to take the order information during init
invite = client.get_invitation(id=conference.get_submission_id())
invite.reply['content']['author_identity_visibility']['order'] = 4
print(invite.reply['content'])
client.post_invitation(invite)


