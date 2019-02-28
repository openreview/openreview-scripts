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

# 12/17/18 17:00 UTC
submission_invitation = conference.open_submissions(due_date = datetime.datetime(2019, 4, 14, 17, 00), additional_fields = {
        'ORCID': {
            'value-regex': '.{0,500}',
            'description': 'Author ORCID identifier',
        },
        'html': {
            'description': 'A link to more information (link must begin with http(s)) (Optional)',
            'value-regex': '(http|https):\/\/.+',
            'required':False
        }
    })

submission_invitation.reply['content']['ORCID']['order'] = 4
submission_invitation.reply['content']['keywords']['order'] = 5
submission_invitation.reply['content']['TL;DR']['order'] = 6
submission_invitation.reply['content']['abstract']['order'] = 7
submission_invitation.reply['content']['html']['order'] = 8

del submission_invitation.reply['content']['pdf']
client.post_invitation(submission_invitation)

