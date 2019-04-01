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
conference.set_program_chairs([
#hidden
])
conference.set_reviewers([
#hideen
])
conference.open_submissions(due_date = datetime.datetime(2019, 4, 13, 12, 0), remove_fields = ['TL;DR'], additional_fields = {
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'required': False,
            'value-regex': 'upload'
        },
        'track': {
            'description': 'Track options',
			'value-radio': ['long (30 minutes)', 'short (15 minutes)', 'discussion topic (5 minutes)'],
			'required':True
        }
})





