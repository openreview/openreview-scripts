#!/usr/bin/python

import sys, os
import argparse
import openreview
from openreview import tools
from openreview import invitations
import config
sys.path.insert(0, "../Full/python")
import full
#sys.path.insert(0,"../Abstract/python")
#import abstract

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

def create_new_group(group_id, group_params):
    # create group if it doesn't already exist
    try:
        group = client.get_group(group_id)
    except openreview.OpenReviewException as e:
        g = openreview.Group(**group_params)
        group = client.post_group(g)
        print("post group " + group_id)
    return group

def setup_parent_conference():
    '''
    set up the conference groups
    '''
    conference_group = openreview.Group(**config.conference_params)
    groups = tools.build_groups(conference_group.id)
    g_params = {
        'readers': ['everyone'],
        'writers': [],
        'signatures': [],
        'signatories': [],
        'members': []
    }
    for g in groups:
        print(g.id)
        g_params['id'] = g.id
        create_new_group(g.id, g_params)

    # Create PCs if needed
    create_new_group(config.PROGRAM_CHAIRS, config.program_chairs_params)


def setup_track(track):


    '''
    Add homepage  add to the conference group.
    '''
    this_conference = create_new_group(track.TRACK_ID, track.track_params)
    this_conference.add_webfield(track.WEBPATH)
    this_conference = client.post_group(this_conference)
    print("adding webfield to", this_conference.id)

    '''
    Set up the first couple groups that are needed before submission.
    e.g. Reviewers, Area Chairs

    The Reviewers and Area Chairs groups will need to exist before we can
    send out recruitment emails.
    '''
    groups = {}
    groups[track.REVIEWERS] = openreview.Group(track.REVIEWERS, **track.group_params)
    for g in groups.values():
        # check group exists first
        try:
            group_exist = client.get_group(g.id)
        except openreview.OpenReviewException as e:
            client.post_group(g)
            print("post group " + g.id)

    '''
    Create submission and comment invitations.
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
        'content': track.submission_content
    }

    submission_inv = openreview.Invitation(track.SUBMISSION, duedate=track.SUBMISSION_TIMESTAMP, **track.submission_params, reply=submission_reply)
    submission_inv = client.post_invitation(submission_inv)
    print("posted invitation "+submission_inv.id)

    comment_inv = invitations.Comment(
        conference_id = track.TRACK_ID,
        process='..' + track.TRACK_NAME + '/process/commentProcess.js',
        invitation = track.SUBMISSION,
    )
    comment_inv.reply['nonreaders'] = {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
    comment_inv = client.post_invitation(comment_inv)
    print("posted invitation "+comment_inv.id)


##############################

setup_parent_conference()
setup_track(full)
#setup_track(abstract)