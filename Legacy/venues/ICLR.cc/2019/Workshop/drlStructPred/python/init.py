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
#conference.set_program_chairs(emails = [
#hidden emails
#])

# March 22, 11:59pm AoE
submission_inv = conference.open_submissions(due_date = datetime.datetime(2019, 3, 23, 11, 59))
submission_inv.reply['content']['authorids']['description']+=" Please provide real emails; identities will be anonymized."
submission_inv.reply['content']['authors']['description']+=" Please provide real names; identities will be anonymized."
submission_inv = client.post_invitation(submission_inv)
