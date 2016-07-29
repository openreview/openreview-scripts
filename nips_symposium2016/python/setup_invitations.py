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
        'abstract': {
            'description': 'Abstract of paper.',
            'order': 4,
            'value-regex': '[\\S\\s]{1,5000}'
        },
        'author_emails': {
            'description': 'Comma separated list of author email addresses, in the same order as above.',
            'order': 2,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'authors': {
            'description': 'Comma separated list of author names, as they appear in the paper.',
            'order': 1,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'conflicts': {
            'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
            'order': 100,
            'value-regex': '^([a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))+(;[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))*$'
        },
        'keywords': {
            'description': 'Comma separated list of keywords.',
            'order': 5,
            'values-regex': '.*'
        },
        'pdf': {
            'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv.',
            'order': 4,
            'value-regex': 'upload|http://arxiv.org/pdf/.+'
        },
        'title': {
            'description': 'Title of paper.',
            'order': 3,
            'value-regex': '.{1,100}'
        }
    }
}
submission_invitation = Invitation( 'NIPS/Symposium/2016',
    'submission', 
    writers     = ['NIPS/Symposium/2016'],
    readers     = ['everyone'], 
    invitees    = ['~'], 
    reply       = submission_reply, 
    process     = '../process/submissionProcess_nips_symposium2016.js',
    signatures  = ['NIPS/Symposium/2016'])

invitations = [submission_invitation]

## Post the invitations
for i in invitations:
    print "Posting invitation: "+i.body['id']
    openreview.save_invitation(i.body)




# note_writer = openreview.get_group('signatory'=openreview.user['id'], 'regex'='~.*'})
# print "note authored by "+note_writer

# ## Define and post a sample note
# note1 = {
#     'content': {
#         'CMT_id':'',
#         'abstract':'This is note 1',
#         'author_emails':"author@gmail.com",
#         'authors':'Author 1',
#         'conflicts':'cs.berkeley.edu',
#         'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
#         'title':'Note 1',
#         'keywords':['keyword']
#     },
#     'forum': None,
#     'invitation': 'NIPS/Symposium/2016/-/submission',
#     'parent': None,
#     'pdfTransfer':"url",
#     'readers':["everyone"],
#     'signatures':[note_writer],
#     'writers':[note_writer]
# }

# openreview.set_note(note1)