#!/usr/bin/python

import argparse
import openreview
from openreview import tools
from openreview import invitations
from openreview import webfield
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

print config.CONFERENCE_ID

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)
'''
set up the conference groups
'''
conference_group = openreview.Group(**config.conference_params)
groups = tools.build_groups(conference_group.id)
for g in groups:
    # TODO check group exists first
    try:
        group_exist = client.get_group(g.id)
    except openreview.OpenReviewException as e:
        client.post_group(g)
        print "post group "+g.id

'''
Create the homepage and add it to the conference group.
'''

homepage = webfield.Webfield(
	config.HOMEPAGE_TEMPLATE,
    group_id = config.CONFERENCE_ID,
    js_constants = config.JS_CONSTANTS,
)

this_conference = client.get_group(config.CONFERENCE_ID)
this_conference.web = homepage.render()
this_conference = client.post_group(this_conference)
print "adding webfield to", this_conference.id

filename = config.HOMEPAGE_TEMPLATE.split('.template')[0]+'.js'
f = open(filename, 'w')
f.write(this_conference.web)
f.close()

'''
Set up the first couple groups that are needed before submission.
e.g. Program Chairs, Reviewers

The Reviewers groups will need to exist before we can
send out recruitment emails.

'''
groups = {}
groups[config.PROGRAM_CHAIRS] = openreview.Group(config.PROGRAM_CHAIRS, **config.program_chairs_params)
groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.group_params)
for g in groups.values():
	print "Posting group: ", g.id
	client.post_group(g)

'''
Create a submission and comment invitations.
'''

submission_inv = invitations.Submission(
    conference_id = config.CONFERENCE_ID,
    duedate = config.SUBMISSION_TIMESTAMP,
	process = '../process/submissionProcess.js',
    reply_params={
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [config.CONFERENCE_ID, config.PROGRAM_CHAIRS, '{content.authorids}', '{signatures}']
        }
    }
)

submission_inv = client.post_invitation(submission_inv)
print "posted invitation "+submission_inv.id

blind_submission_inv = invitations.Submission(
    id = config.BLIND_SUBMISSION,
    conference_id = config.CONFERENCE_ID,
    duedate = config.SUBMISSION_TIMESTAMP,
    mask = {
        'authors': {
            'values': ['Anonymous']
        },
        'authorids': {
            'values-regex': '.*'
        }
    },
    reply_params={
        'signatures': {'values': [config.CONFERENCE_ID]},
        'readers': {'values': ['everyone']}
    }
)
blind_submission_inv = client.post_invitation(blind_submission_inv)
print "posted invitation "+blind_submission_inv.id

comment_inv = invitations.Comment(
    conference_id = config.CONFERENCE_ID,
	process='../process/commentProcess.js',
    invitation = config.BLIND_SUBMISSION,
)
comment_inv = client.post_invitation(comment_inv)
print "posted invitation "+comment_inv.id



