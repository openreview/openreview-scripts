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
conference.set_program_chairs([
#hidden
])
conference.set_reviewers([
#hidden
])

# on May 31st, change pdf to required
conference.open_submissions(due_date = datetime.datetime(2019, 6, 4, 23, 59), remove_fields = ['TL;DR'], additional_fields = {
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'required': False,
            'value-regex': 'upload'
        }
})