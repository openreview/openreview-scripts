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

# Authors have the option to be anonymized.
# When submissions are closed, some blinded notes will actually have all of the information
# from submissions, and some will be blinded in the normal fashion.
conference.open_submissions(due_date = datetime.datetime(2019, 4, 15, 23, 59), additional_fields = {
        "anonymized": {
            "order": 11,
            "value-checkbox": "Anonymize author identities",
            "required": False
        }
    })


