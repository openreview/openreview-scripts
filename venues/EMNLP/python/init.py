#!/usr/bin/python

import argparse
import openreview
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

emnlp_request_id = 'rylllwkbKN'
start_date = datetime.datetime(2019, 4, 2, 13, 30)
due_date = datetime.datetime(2019, 8, 19, 23, 59)

conference = openreview.helpers.get_conference(client, emnlp_request_id)

author_consent_agreement = (
    '**IMPORTANT: PLEASE READ**\n\n'
    'The workshop is collecting a research dataset containing a set of peer'
    'reviews for research purposes. This dataset may be released to the '
    'public domain six months after the final accept/reject decisions are made. '
    'Do you agree to include your reviews in this dataset?'
)

additional_fields = {
    "consent": {
        "value-radio": [
                "Yes, include my anonymized reviews in the \"workshop research dataset\".",
                "No. Do not include my reviews in the \"workshop research dataset\"."
        ],
        "default": "Yes, include my anonymized reviews in the \"workshop research dataset\".",
        "description": author_consent_agreement,
        "scroll": True
    }
}

conference.open_submissions(
    start_date=start_date,
    due_date=due_date,
    additional_fields=additional_fields)

