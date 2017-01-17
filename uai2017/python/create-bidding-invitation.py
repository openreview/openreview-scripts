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

bidding_main_invitation = openreview.Invitation('auai.org/UAI/2017', 'main_bidding',
    readers = ['auai.org/UAI/2017'],
    writers = ['auai.org/UAI/2017'],
    invitees = ['OpenReview.net'],
    signatures = ['auai.org/UAI/2017'],
    process = '../process/mainBidProcess.js')

bidding_main_invitation.reply = {
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
        'values': [COCHAIRS, SPC, PC]
    },
    "signatures":{
        'values': ['auai.org/UAI/2017']
    },
    "writers":{
        'values': ['auai.org/UAI/2017']
    }
}

client.post_invitation(bidding_main_invitation)

bidding_rootnote = openreview.Note(invitation='auai.org/UAI/2017/-/main_bidding',
    readers = [COCHAIRS, SPC, PC],
    writers = ['auai.org/UAI/2017'],
    signatures = ['auai.org/UAI/2017'])
bidding_rootnote.content = {
    'title': 'Paper Bidding',
    'description': "Please submit 50 paper biddings."
}

#Create a note if not present
notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/main_bidding')
root_note = None
if not notes:
    print 'Posting root note'
    root_note = client.post_note(bidding_rootnote)
else:
    root_note = notes[0]

bidding_invitation = openreview.Invitation('auai.org/UAI/2017', 'paper_bidding',
    duedate = 1507226400000,
    readers = ['everyone'],
    writers = ['auai.org/UAI/2017'],
    invitees = [PC],
    signatures = ['auai.org/UAI/2017'],
    process = '../process/bidProcess.js')



submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
content = {
    'title': {
        'order': 1,
        'value': 'Paper Bids'
    }
}
order = 2
for submission in submissions:
    content['Paper ' + str(submission.number)] = {
        'order': order,
        'value-radio': [
            'I want to review',
            'I can review',
            'I can probably review but am not an expert',
            'I cannot review'
        ],
        'description': submission.content['title']
    }

    order += 1


bidding_invitation.reply = {
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

client.post_invitation(bidding_invitation)

