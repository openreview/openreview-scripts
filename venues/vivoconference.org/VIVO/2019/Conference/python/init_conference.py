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
submission_invitation = conference.open_submissions(due_date = datetime.datetime(2019, 4, 14, 17, 00), public = True, additional_fields = {
        'html': {
            'description': 'Provide a direct url to your artifact (link must begin with http(s)) (Optional)',
            'order': 8,
            'value-regex': '(http|https):\/\/.+',
            'required':False
        }
    })

submission_invitation.reply['content']['keywords']['order'] = 4
submission_invitation.reply['content']['TL;DR']['order'] = 5
submission_invitation.reply['content']['abstract']['order'] = 6
submission_invitation.reply['content']['pdf']['order'] = 7
submission_invitation.reply['content']['pdf']['required'] = False
submission_invitation.reply['content']['html']['order'] = 8
submission_invitation.reply['content']['pdf']['description'] = ['Upload a PDF file that ends with .pdf (Optional)']
with open('../process/submissionProcess.js','r') as f:
    submission_invitation.process = f.read()
client.post_invitation(submission_invitation)



print ("Adding Program Chair group")
pc_emails = ['muniyal@cs.umass.edu']
conference.set_program_chairs(pc_emails)


reviewer_emails = []
conference.set_reviewers(reviewer_emails)
conference.recruit_reviewers()
reviewer_grp = client.get_group('vivoconference.org/VIVO/2019/Conference/Reviewers')
readers = reviewer_grp.readers
readers.append('vivoconference.org/VIVO/2019/Conference/Program_Chairs')
reviewer_grp.readers = readers
client.post_group(reviewer_grp)