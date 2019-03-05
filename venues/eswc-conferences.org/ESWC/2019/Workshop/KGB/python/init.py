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

# 3/1/19 23:59 Hawaii time
conference.open_submissions(due_date = datetime.datetime(2019, 3, 12, 9, 59), additional_fields = {
        'contribution': {
            'order': 5,
            'value-dropdown': [
                'Full research papers (8-12 pages)',
                'In Use and Experience papers (8-12 pages)',
                'Position papers (6-8 pages)',
                'Short research papers (4-6 pages)',
                'System or Demo papers (4-6 pages)'
            ],
            'required': True
        },
        'html': {
            'description': 'Either provide a direct url to your artifact (link must begin with http(s)) or upload a PDF file',
            'order': 8,
            'value-regex': '(http|https):\/\/.+',
            'required': False
        },
        'pdf': {
            'order': 9,
            'value-regex': 'upload',
            'required': False
        }
    })
