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
    builder = openreview.conference.ConferenceBuilder(client)
    builder.set_conference_id('MIDL.io/2019/Conference')
    builder.set_conference_name('Medical Imaging with Deep Learning')
    builder.set_homepage_header({
    'title': 'Medical Imaging with Deep Learning',
    'subtitle': 'MIDL 2019 Conference',
    'deadline': 'Submission Deadline: 13th of December, 2018',
    'date': '8-10 July 2019',
    'website': 'http://2019.midl.io',
    'location': 'London',
    'instructions': 'Full papers contain well-validated applications or methodological developments of deep learning algorithms in medical imaging. There is no strict limit on paper length. However, we strongly recommend keeping full papers at 8 pages (excluding references and acknowledgements). An appendix section can be added if needed with additional details but must be compiled into a single pdf. The appropriateness of using pages over the recommended page length will be judged by reviewers. All accepted papers will be presented as posters with a selection of these papers will also be invited for oral presentation.'
    })
    builder.set_conference_type(openreview.builder.SingleBlindConferenceType)
    conference = builder.get_result()


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
