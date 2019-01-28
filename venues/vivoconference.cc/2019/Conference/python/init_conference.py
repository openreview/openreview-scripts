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
conference.open_submissions(due_date = datetime.datetime(2019, 3, 5, 17, 00), public = False, additional_fields = {
        'html': {
            'fieldDisplayLabel': 'Html',
            'description': 'Provide a direct url to your artifact (link must begin with http(s)) (Optional)',
            'order': 7,
            'value-regex': '(http|https):\/\/.+',
            'required':False
        }
    })
