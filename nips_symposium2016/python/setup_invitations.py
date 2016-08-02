#!/usr/bin/python

###############################################################################
#
###############################################################################

## Import statements
import argparse
import csv
import getpass
import json
import sys
sys.path.append('../..')
from client import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
args = parser.parse_args()

## Initialize the client library with username and password
openreview = Client(config='./nips_symposium2016_config.ini')
base_url = openreview.base_url

## Create the submission invitation
submission_reply = {
    'forum': None,
    'parent': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
    },
    'writers': {
        'values-regex': '~.*'
    },
    'content': {
        'title': {
            'description': 'Title of paper.',
            'order': 1,
            'value-regex': '.{1,100}'
        },
        'authors': {
            'description': 'Comma separated list of author names, as they appear in the paper.',
            'order': 2,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'author_emails': {
            'description': 'Comma separated list of author email addresses, in the same order as above.',
            'order': 3,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'abstract': {
            'description': 'Abstract of paper.',
            'order': 4,
            'value-regex': '[\\S\\s]{0,5000}'
        },
        'pdf': {
            'description': 'Provide a direct link to your PDF (must have a .pdf extension)',
            'order': 5,
            'value-regex': 'upload|http://arxiv.org/pdf/.+'
        }
    }
}
submission_invitation = Invitation('NIPS.cc/Symposium/2016',
    'submission', 
    writers     = ['NIPS.cc/Symposium/2016'],
    readers     = ['everyone'], 
    invitees    = ['~'], 
    reply       = submission_reply, 
    process     = '../process/submissionProcess_nips_symposium2016.js',
    signatures  = ['NIPS.cc/Symposium/2016'])

invitations = [submission_invitation]

## Post the invitations
for i in invitations:
    print "Posting invitation: "+i.id
    openreview.save_invitation(i)



note_writer = openreview.get_groups(signatory=openreview.user['id'], prefix='~')[0].to_json()['id']
print "Posting sample note with author "+note_writer

## Define and post a sample note
sample_note = Note(content=
    {
        'CMT_id':'',
        'abstract':'This is a sample note to test the process functions for the invitation to which this note responds.',
        'author_emails':"author@gmail.com",
        'authors':'Author 1',
        'conflicts':'cs.berkeley.edu',
        'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
        'title':'Sample Note'
    },
    forum=None,
    invitation='NIPS.cc/Symposium/2016/-/submission',
    parent=None,
    pdfTransfer="url",
    readers=["everyone"],
    signatures=[note_writer],
    writers=[note_writer]
)

openreview.save_note(sample_note)