#!/usr/bin/python

"""
Initializes the structures used for paper/reviewer metadata
"""

## Import statements
import argparse
import csv
import sys
import openreview

from uaidata import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


#Gather variables to be used downstream
submissions = client.get_notes(invitation=CONFERENCE+"/-/blind-submission")


#Create the paper metadata invitation
paper_metadata_reply = {
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
    'content': {} #content is blank; this allows for ANYTHING to be placed in the content field.
    #we'll want to change this later one we know what the format will be.
}
paper_metadata_invitation = openreview.Invitation('auai.org/UAI/2017','Paper/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=paper_metadata_reply)
client.post_invitation(paper_metadata_invitation)


#Create the reviewer metadata invitation
reviewer_metadata_reply = {
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
    'content': {} #Content is blank. See above.
}
reviewer_metadata_invitation = openreview.Invitation('auai.org/UAI/2017','Reviewer/Metadata',
                                           writers=['OpenReview.net'],
                                           readers=['OpenReview.net'],
                                           invitees=['OpenReview.net'],
                                           signatures=['OpenReview.net'],
                                           reply=reviewer_metadata_reply)
client.post_invitation(reviewer_metadata_invitation)







#Pre-populate all the paper metadata notes
for n in submissions:
    print "generating note for paper %s" % n.id

    note = openreview.Note(
        invitation = CONFERENCE + "/-/Paper/Metadata",
        readers = [COCHAIRS, ADMIN],
        forum = n.id,
        writers = ['OpenReview.net'],
        content = {'reviewers':[], 'papers':[]},
        signatures = [ADMIN]
    )

    client.post_note(note)

# #Pre-populate all the reviewer metadata notes
reviewers = client.get_group(PC)
for g in reviewers.members:
    note = openreview.Note(
        invitation=CONFERENCE + "/-/Reviewer/Metadata",
        readers=[COCHAIRS, ADMIN],
        writers=['OpenReview.net'],
        content={'name':g, 'reviewers':[]},
        signatures=[ADMIN]
    )
    client.post_note(note)
