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
submission_invitation = conference.open_submissions(due_date = datetime.datetime(2050, 1, 1, 22, 00), public = True, additional_fields = {
        'artifact type': {
            'fieldDisplayLabel': 'Artifact Type',
            'description': 'Type of the artifact.',
            'order': 5,
            'values-dropdown': [
                'Code',
                'Dataset',
                'User study log book',
                'Other'
            ],
            'required': True
        },
        'requested badges': {
            'fieldDisplayLabel': 'Requested Badges',
            'description': 'Please select all the badges that you are requesting for.',
            'order': 6,
            'values-dropdown': [
                'Artifacts Available',
                'Artifacts Evaluated – Functional and Reusable',
                'Results Replicated',
                'Results Reproduced'
            ],
            'required': True
        },
        'html': {
            'fieldDisplayLabel': 'Html',
            'description': 'Either provide a direct url to your artifact (link must begin with http(s)) or upload a PDF file',
            'order': 7,
            'value-regex': '(http|https):\/\/.+',
            'required':False
        },
        'pdf': {
            'fieldDisplayLabel': 'PDF',
            'order': 8,
            'value-regex': 'upload',
            'required':False
        }
    }, include_keywords = False, include_TLDR = False)

#Override process function
with open('../process/submissionProcess.js') as f:
    submission_invitation.readers = [conference.get_authors_id()]
    submission_invitation.process = f.read()
    client.post_invitation(submission_invitation)

conference.set_program_chairs(emails = []) # paste real emails
conference.set_reviewers(emails = []) # past real emails

# Override author group
author_group = openreview.Group(id = conference.get_authors_id(),
    readers = [conference.get_program_chairs_id()],
    writers = [conference.get_program_chairs_id()],
    signatories = [[conference.get_authors_id()]],
    signatures = [conference.get_id()],
    members = ['spector@cs.umass.edu'])
client.post_group(author_group)

# Badging decision invitation for Chairs
badging_decision_inv = openreview.Invitation(
    id = conference.get_id() + '/-/Decision',
    duedate = 1575732251000, #GMT: Saturday, December 7, 2019 3:24:11 PM
    readers = ['everyone'],
    writers = [conference.get_id()],
    signatures = [conference.get_id()],
    invitees = [conference.get_program_chairs_id()],
    multiReply = True,
    taskCompletionCount = 1000,
    reply = {
        'invitation': conference.get_id() + '/-/Submission',
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values-regex': '~.*'
        },
        'content':{
            'tag': {
                'description': 'Artifact Badge decision',
                'order': 1,
                'values-dropdown': ['No Badges', 'Artifacts Available', 'Artifacts Evaluated – Functional and Reusable', 'Results Replicated', 'Results Reproduced'],
                'required': True
            }
        }
    },
    web = '../webfield/decisionWebfield.js'
)

client.post_invitation(badging_decision_inv)

