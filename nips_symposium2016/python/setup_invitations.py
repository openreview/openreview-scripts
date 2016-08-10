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

## Create the recommendation invitation
recommendation_reply = {
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
            'order': 2,
            'value-regex': '.{1,100}'
        },
        'authors': {
            'description': 'Comma separated list of author names, as they appear in the paper.',
            'order': 3,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'author_emails': {
            'description': 'Optional: please provide the e-mail address of one or more of the authors.',
            'order': 4,
            'value-regex': '.*'
        },
        'abstract': {
            'description': 'Abstract of paper.',
            'order': 5,
            'value-regex': '[\\S\\s]{0,5000}'
        },
        'pdf': {
            'description': 'Provide a direct link to your PDF (link must begin with http(s):// and end with .pdf extension)',
            'order': 1,
            'value-regex': '(http|https):\/\/.+\.pdf'
        }
    }
}
recommendation_invitation = Invitation('NIPS.cc/2016/Deep_Learning_Symposium',
    'recommendation', 
    writers     = ['NIPS.cc/2016/Deep_Learning_Symposium'],
    readers     = ['everyone'], 
    invitees    = ['~'], 
    reply       = recommendation_reply, 
    process     = '../process/recommendationProcess_nips_symposium2016.js',
    signatures  = ['NIPS.cc/2016/Deep_Learning_Symposium'])

invitations = [recommendation_invitation]

## Post the invitations
for i in invitations:
    print "Posting invitation: "+i.id
    openreview.post_invitation(i)