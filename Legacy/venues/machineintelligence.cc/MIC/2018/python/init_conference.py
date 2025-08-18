#!/usr/bin/python

import sys, os
import argparse
import openreview
from openreview import tools
from openreview import invitations
from openreview import webfield

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
	print "Track required: either 'Abstract' or 'Conference'"
	print "Cannot locate config.py in:"+config_path
	sys.exit()
## load conference specific data
sys.path.insert(0, config_path)
import config

print config.CONFERENCE_ID

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)
'''
set up the conference groups
'''
conference_group = openreview.Group(**config.conference_params)
groups = tools.post_group_parents(client, conference_group, overwrite_parents=True)

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

# TODO PAM, save webfield as file ending in .js

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
	print "Posting group: ", g.id
	client.post_group(g)

'''
Create a submission and comment invitations.
'''

submission_inv = invitations.Submission(
    conference_id = config.CONFERENCE_ID,
    duedate = config.SUBMISSION_TIMESTAMP,
	process = '../'+args.track+'/process/submissionProcess.js',
    content_params = config.submission_content_overwrite
)
submission_inv = client.post_invitation(submission_inv)
print "posted invitation "+submission_inv.id

comment_inv = invitations.Comment(
    conference_id = config.CONFERENCE_ID,
	process='../' + args.track + '/process/commentProcess.js',
    invitation = config.SUBMISSION,
)
comment_inv = client.post_invitation(comment_inv)
print "posted invitation "+comment_inv.id



