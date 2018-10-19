#!/usr/bin/python

import sys, os
import argparse
import openreview
from openreview import tools
from openreview import invitations

"""
REQUIRED SCRIPT ARGUMENT
	track - either the "Abstract" or "Conference" track
OPTIONAL SCRIPT ARGUMENTS

	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password
"""

parser = argparse.ArgumentParser()
parser.add_argument('track', help="Abstract or Conference")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

config_path = "../"+args.track+"/python/"
if os.path.isfile(config_path+"config.py") is False:
	print("Track required: either 'Abstract' or 'Conference'")
	print("Cannot locate config.py in:"+config_path)
	sys.exit()
## load conference specific data
sys.path.insert(0, config_path)
import config

print(config.CONFERENCE_ID)

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))
'''
set up the conference groups
'''
conference_group = openreview.Group(**config.conference_params)
groups = tools.build_groups(conference_group.id)
for g in groups:
    # check group exists first
    try:
        group_exist = client.get_group(g.id)
    except openreview.OpenReviewException as e:
        client.post_group(g)
        print("post group "+g.id)

'''
Add homepage  add to the conference group.
'''
this_conference = client.get_group(config.CONFERENCE_ID)
this_conference.add_webfield(config.WEBPATH)
this_conference = client.post_group(this_conference)
print("adding webfield to", this_conference.id)

'''
Set up the first couple groups that are needed before submission.
e.g. Program Chairs, Reviewers, Area Chairs

The Reviewers and Area Chairs groups will need to exist before we can
send out recruitment emails.
'''
groups = {}
groups[config.PROGRAM_CHAIRS] = openreview.Group(config.PROGRAM_CHAIRS, **config.program_chairs_params)
groups[config.AREA_CHAIRS] = openreview.Group(config.AREA_CHAIRS, **config.group_params)
groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.group_params)
for g in groups.values():
	print("Posting group: ", g.id)
	client.post_group(g)

'''
Create a submission and comment invitations.
'''
submission_reply = {
    'forum': None,
    'replyto': None,
    'invitation': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
    },
    'writers': {
        'values': []
    },
    'content': config.submission_content
}

submission_inv = openreview.Invitation(config.SUBMISSION, duedate=config.SUBMISSION_TIMESTAMP, **config.submission_params, reply=submission_reply)
submission_inv = client.post_invitation(submission_inv)
print("posted invitation "+submission_inv.id)

comment_inv = invitations.Comment(
    conference_id = config.CONFERENCE_ID,
	process='../' + args.track + '/process/commentProcess.js',
    invitation = config.SUBMISSION,
)
comment_inv = client.post_invitation(comment_inv)
print("posted invitation "+comment_inv.id)



