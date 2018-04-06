#!/usr/bin/python

import sys, os
import argparse
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

def build_groups(conference_group_id):
    # create list of subpaths (e.g. Test.com, Test.com/TestConference, Test.com/TestConference/2018)
    path_components = conference_group_id.split('/')
    paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

    empty_params = {
        'readers': ['everyone'],
        'writers': [],
        'signatures': [],
        'signatories': [],
        'members': []
    }

    groups = {p: openreview.Group(p, **empty_params) for p in paths}
    groups[conference_group_id].writers = groups[conference_group_id].signatories = [conference_group_id]

    admin_id = conference_group_id + '/Admin'
    groups[admin_id] = openreview.Group(admin_id, readers=[admin_id], signatories=[admin_id])

    return groups

groups = build_groups(config.CONFERENCE_ID)
for g in sorted([g for g in groups]):
    print "posting group {0}".format(g)
    client.post_group(groups[g])

# Add webfield for parent MIDL group
group = client.get_group('MIDL.amsterdam/2018')
print group.id
with open('../../midl18-landing-webfield.html') as f:
    group.web = f.read()
group.signatures = [client.signature]
updated_group = client.post_group(group)

# add admin group to the conference members
client.add_members_to_group(groups[config.CONFERENCE_ID], config.CONFERENCE_ID + '/Admin')

groups = {}
groups[config.PROGRAM_CHAIRS] = openreview.Group(config.PROGRAM_CHAIRS, **config.program_chairs_params)
groups[config.AREA_CHAIRS] = openreview.Group(config.AREA_CHAIRS, **config.group_params)
groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.group_params)

groups[config.CONFERENCE_ID] = client.get_group(config.CONFERENCE_ID)
groups[config.CONFERENCE_ID].signatures = [client.signature]
groups[config.CONFERENCE_ID].add_webfield(config.WEBPATH)

invitations = {}
invitations[config.SUBMISSION] = openreview.Invitation(config.SUBMISSION, duedate=config.SUBMISSION_TIMESTAMP, **config.submission_params)
invitations[config.COMMENT] = openreview.Invitation(config.COMMENT, **config.comment_params)

invitations[config.SUBMISSION].reply = config.submission_reply
invitations[config.COMMENT].reply = config.comment_reply

for g in groups.values():
	print "Posting group: ", g.id
	client.post_group(g)

for i in invitations.values():
	print "Posting invitation: ", i.id
	client.post_invitation(i)
