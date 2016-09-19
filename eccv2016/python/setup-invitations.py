#!/usr/bin/python

###############################################################################
#
###############################################################################

## Import statements
import argparse
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

submission_reply = {
  'forum': None,
  'replyto': None,
  'signatures': {
    'values-regex': '~.*',
    'description':'Your displayed identity associated with the above content.'
  },
  'writers': {'values-regex': '~.*'},
  'readers': { 
    'values': ['everyone'], 
    'description': 'The users who will be allowed to read the above content.'
  },
  'content': {
    'title': {
      'order': 3,
      'value-regex': '.{1,100}',
      'description': 'Title of paper.'
    },
    'abstract': {
      'order': 4,
      'value-regex': '[\\S\\s]{1,5000}',
      'description': 'Abstract of paper.'
    },
    'authors': {
      'order': 1,
      'value-regex': '[^,\\n]+(,[^,\\n]+)*',
      'description': 'Comma separated list of author names, as they appear in the paper.'
    },
    'author_emails': {
      'order': 2,
      'value-regex': '[^,\\n]+(,[^,\\n]+)*',
      'description': 'Comma separated list of author email addresses, in the same order as above.'
    },
    'conflicts': {
      'order': 100,
      'value-regex': "^([a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))+(;[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))*$",
      'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).'
    },
    'pdf': {
      'order': 4,
      'value-regex': 'upload|http://arxiv.org/pdf/.+',
      'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv.'
    },
    'submit for proceedings':{
      'order':5,
      'value-radio':[
        'yes',
        'no'
      ],
      'description': "Choose whether you would like your submission to appear in the conference proceedings."
    }
  }
}

submission_invitation = Invitation('ECCV2016.org/BNMW','submission',
	readers=['everyone'],
	writers=['ECCV2016.org/BNMW'],
	invitees=['~'],
	signatures=['ECCV2016.org/BNMW'],
	process='../process/bnmwProcess.js',
	reply=submission_reply)

openreview.post_invitation(submission_invitation)
        