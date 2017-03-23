#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import csv
import sys
import openreview

from uaidata import *

# Handle the arguments and initialize openreview client
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


# Create the paper metadata invitations
# .............................................................................
metadata_reply = {
    'forum': None,
    'replyto': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': [COCHAIRS, ADMIN] #who should be allowed to read UAI submissions and when?
    },
    'signatures': {
        'description': 'How your identity will be displayed with the above content.',
        'values-regex': ADMIN
    },
    'writers': {
        'values-regex': 'OpenReview.net'
    },
    'content': {}
}

paper_metadata_invitation = openreview.Invitation(CONFERENCE+'/-/Paper/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=metadata_reply)
client.post_invitation(paper_metadata_invitation)


#Create the reviewer metadata invitation
reviewer_metadata_invitation = openreview.Invitation(CONFERENCE+'/-/Reviewer/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=metadata_reply)
client.post_invitation(reviewer_metadata_invitation)

#Create the user metadata invitation
areachair_metadata_invitation = openreview.Invitation(CONFERENCE+'/-/Area_Chair/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=metadata_reply)
client.post_invitation(areachair_metadata_invitation)


# Main Script
# .............................................................................

overwrite = args.overwrite and args.overwrite.lower()=='true'

submissions = client.get_notes(invitation=CONFERENCE+"/-/blind-submission")
existing_paper_metadata = client.get_notes(invitation=CONFERENCE + "/-/Paper/Metadata")
metadata_by_forum = {n.forum: n for n in existing_paper_metadata}

# Pre-populate all the paper metadata notes
for n in submissions:
    if n.forum not in metadata_by_forum:
        metadata = openreview.Note(
          invitation = CONFERENCE + "/-/Paper/Metadata",
          readers = [COCHAIRS, ADMIN],
          forum = n.id,
          writers = ['OpenReview.net'],
          content = {'reviewers':[], 'areachairs':[], 'papers':[]},
          signatures = [ADMIN]
        )
        client.post_note(metadata)
        print "generating metadata for PAPER %s" % n.forum
    elif overwrite:
        metadata = metadata_by_forum[n.forum]
        metadata.content['reviewers'] = []
        metadata.content['areachairs'] = []
        metadata.content['papers'] = []
        client.post_note(metadata)
        print "resetting metadata for PAPER %s" % n.forum

# Pre-populate all the reviewer metadata notes
reviewers = client.get_group(PC).members
existing_reviewer_metadata = client.get_notes(invitation = CONFERENCE + "/-/Reviewer/Metadata")
metadata_by_reviewer = {u.content['name']: u for u in existing_reviewer_metadata}

for r in reviewers:
    if r not in metadata_by_reviewer:
        metadata = openreview.Note(
            invitation=CONFERENCE + "/-/Reviewer/Metadata",
            readers=[COCHAIRS, ADMIN],
            writers=['OpenReview.net'],
            content={'name':r, 'reviewers':[]},
            signatures=[ADMIN]
        )
        client.post_note(metadata)
        print "generating metadata for REVIEWER %s" % r
    elif overwrite:
        metadata = metadata_by_reviewer[r]
        metadata.content['reviewers'] = []
        client.post_note(metadata)
        print "resetting metadata for REVIEWER %s" %r


# Pre-populate all the area chair metadata notes
areachairs = client.get_group(SPC).members
existing_areachair_metadata = client.get_notes(invitation = CONFERENCE + "/-/Area_Chair/Metadata")
metadata_by_areachair = {u.content['name']: u for u in existing_areachair_metadata}

for a in areachairs:
    if a not in metadata_by_areachair:
        metadata = openreview.Note(
            invitation=CONFERENCE + "/-/Area_Chair/Metadata",
            readers=[COCHAIRS, ADMIN],
            writers=['OpenReview.net'],
            content={'name':a, 'areachairs':[]},
            signatures=[ADMIN]
        )
        client.post_note(metadata)
        print "generating metadata for AREACHAIR %s" % a
    elif overwrite:
        metadata = metadata_by_areachair[a]
        metadata.content['areachairs'] = []
        client.post_note(metadata)
        print "resetting metadata for AREACHAIR %s" % a
