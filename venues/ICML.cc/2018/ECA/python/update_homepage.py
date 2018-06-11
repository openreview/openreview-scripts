#!/usr/bin/python

import sys, os
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
