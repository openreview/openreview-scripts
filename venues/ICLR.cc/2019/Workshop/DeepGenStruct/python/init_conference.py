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
conference.open_submissions(due_date = datetime.datetime(2019, 3, 16, 0, 0))

'''
Create the homepage and add it to the conference group.
'''
conf_group = client.get_group(conference.get_id())
conf_group.add_webfield('../webfield/conferenceWebfield.js')
conf_group = client.post_group(conf_group)
print("added webfield to", conf_group.id)


'''
Update process function on submission for blind submission
'''
submission_inv =client.get_invitation(conference.get_submission_id())
with open('../process/submissionProcess.js') as f:
    submission_inv.process = f.read()

submission_inv.reply['content']['authorids']['description']+=" Please provide real emails; identities will be anonymized."
submission_inv.reply['content']['authors']['description']+=" Please provide real names; identities will be anonymized."
submission_inv = client.post_invitation(submission_inv)
print("posted invitation "+submission_inv.id)

blind_submission_inv = invitations.Submission(
    id = config.BLIND_SUBMISSION,
    conference_id = conference.get_id(),
    duedate = submission_inv.duedate,
    mask = {
        'authors': {
            'values': ['Anonymous']
        },
        'authorids': {
            'values-regex': '.*'
        }
    },
    reply_params={
        'signatures': {'values': [conference.get_id()]},
        'readers': {'values': ['everyone']}
    }
)
blind_submission_inv = client.post_invitation(blind_submission_inv)
print("posted invitation "+blind_submission_inv.id)



