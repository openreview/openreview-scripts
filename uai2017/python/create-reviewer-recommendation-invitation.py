#!/usr/bin/python

###############################################################################
# Not to spec
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
import re
import openreview
import requests
from uaidata import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
baseurl = client.baseurl

COCHAIRS = UAIData.get_program_co_chairs()
PC = UAIData.get_program_committee()
SPC = UAIData.get_senior_program_committee()

recommendation_main_invitation = openreview.Invitation('auai.org/UAI/2017', 'Main_Reviewer_Recommendation',
    readers = ['auai.org/UAI/2017'],
    writers = ['auai.org/UAI/2017'],
    invitees = ['OpenReview.net'],
    signatures = ['auai.org/UAI/2017'],
    process = '../process/emptyProcess.js')

recommendation_main_invitation.reply = {
    "content": {
        'title': {
            'description': 'Title.',
            'order': 1,
            'value-regex': '.{1,250}',
            'required':True
        },
        'description': {
            'order': 2,
            'value-regex': '[\\S\\s]{1,5000}',
            'required':True
        },
    },
    "readers":{
        'values': [COCHAIRS, SPC]
    },
    "signatures":{
        'values': ['auai.org/UAI/2017']
    },
    "writers":{
        'values': ['auai.org/UAI/2017']
    }
}

print 'POST invitation: ', recommendation_main_invitation.id
client.post_invitation(recommendation_main_invitation)

recommendation_rootnote = openreview.Note(invitation='auai.org/UAI/2017/-/Main_Reviewer_Recommendation',
    readers = [COCHAIRS, SPC],
    writers = ['auai.org/UAI/2017'],
    signatures = ['auai.org/UAI/2017'])
recommendation_rootnote.content = {
    'title': 'Reviewer recommendation',
    'description': "Please submit 50 reviewer recommendations."
}

#Create a note if not present
notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Main_Reviewer_Recommendation')
root_note = None
if not notes:
    print 'Posting root note'
    root_note = client.post_note(recommendation_rootnote)
else:
    root_note = notes[0]


recommendation_invitation = openreview.Invitation('auai.org/UAI/2017', 'Paper_Reviewer_Recommendation',
    duedate = 1507226400000,
    readers = ['everyone'],
    writers = ['auai.org/UAI/2017'],
    invitees = [SPC],
    signatures = ['auai.org/UAI/2017'],
    process = '../process/bidProcess.js')



submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
pc_group = client.get_group(PC)

content = {
    'title': {
        'order': 1,
        'value': 'Reviewer recommendations'
    }
}
order = 2
for submission in submissions:
    content['Paper_' + str(submission.number)] = {
        'order': order,
        'values-dropdown': pc_group.members,
        'description': submission.content['title']
    }

    order += 1


recommendation_invitation.reply = {
    "forum": root_note.id,
    "replyto": root_note.id,
    'signatures': {
        'values-regex':'~.+',
        'description': 'How your identity will be displayed with the above content.'
    },
    'writers': {'values-regex':'~.+'},
    'readers': {
        'values': ['auai.org/UAI/2017', COCHAIRS],
        'description': 'The users who will be allowed to read the above content.'
    },
    'content': content
}

print 'POST invitation: ', recommendation_invitation.id
client.post_invitation(recommendation_invitation)

