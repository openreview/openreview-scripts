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
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)
baseurl = openreview.baseurl

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
            'description': 'Provide a direct link to your PDF (must be a arXiv link with .pdf extension)',
            'order': 5,
            'value-regex': 'http://arxiv.org/pdf/.+'
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
    openreview.post_invitation(i)