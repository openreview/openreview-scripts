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


#Gather variables to be used downstream
submissions = client.get_notes(invitation=CONFERENCE+"/-/blind-submission")


#Create the paper metadata invitation
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

paper_metadata_invitation = openreview.Invitation(CONFERENCE,'Paper/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=metadata_reply)
client.post_invitation(paper_metadata_invitation)


#Create the user metadata invitation
user_metadata_invitation = openreview.Invitation(CONFERENCE,'User/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=metadata_reply)
client.post_invitation(user_metadata_invitation)



# Pre-populate all the paper metadata notes
for n in submissions:
    print "generating note for paper %s" % n.id

    note = openreview.Note(
        invitation = CONFERENCE + "/-/Paper/Metadata",
        readers = [COCHAIRS, ADMIN],
        forum = n.id,
        writers = ['OpenReview.net'],
        content = {'users':[], 'papers':[]},
        signatures = [ADMIN]
    )

    client.post_note(note)

# Pre-populate all the user metadata notes
reviewers = client.get_group(PC).members
areachairs = client.get_group(SPC).members
users = reviewers + areachairs
for r in users:
    note = openreview.Note(
        invitation=CONFERENCE + "/-/User/Metadata",
        readers=[COCHAIRS, ADMIN],
        writers=['OpenReview.net'],
        content={'name':r, 'users':[]},
        signatures=[ADMIN]
    )
    client.post_note(note)

