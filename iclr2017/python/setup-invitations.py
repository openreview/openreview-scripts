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

## Create the submission invitation
reply = {
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
            'order': 3,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'authors': {
            'description': 'Comma separated list of author names, as they appear in the paper.',
            'order': 2,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*'
        },
        'conflicts': {
            'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
            'order': 100,
            'value-regex': '^$|([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)(\;[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)*'
        },
        'keywords': {
            'description': 'Comma separated list of keywords.',
            'order': 6,
            'values-regex': '.*'
        },
        'pdf': {
            'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv (link must begin with http(s) and end with .pdf)',
            'order': 5,
            'value-regex': 'upload|(http|https):\/\/.+\.pdf'
        },
        'title': {
            'description': 'Title of paper.',
            'order': 1,
            'value-regex': '.{1,100}'
        }
    }
}

submission_reply=reply.copy()
submission_reply['referenti']=['ICLR.cc/2017/conference/-/reference']

submission_invitation = Invitation( 'ICLR.cc/2017/conference',
    'submission', 
    readers=['everyone'], 
    writers=['ICLR.cc/2017/conference'],
    invitees=['~'], 
    signatures=['ICLR.cc/2017/pcs'], 
    reply=submission_reply, 
    process='../process/submissionProcess_iclr2017.js')

reference_reply=reply.copy()

reference_invitation = Invitation('ICLR.cc/2017/conference',
    'reference',
    readers=['everyone'], 
    writers=['ICLR.cc/2017/conference'],
    invitees=['~'], 
    signatures=['ICLR.cc/2017/pcs'], 
    reply=reference_reply)


## Create 'request for availability to review' invitation
reviewer_invitation_reply = {
    'content': {
        'email': {
            'description': 'Email address.',
            'order': 1,
            'value-regex': '\\S+@\\S+\\.\\S+'
        },
        'key': {
            'description': 'Email key hash',
            'order': 2,
            'value-regex': '.{0,100}'
        },
        'response': {
            'description': 'Invitation response',
            'order': 3,
            'value-radio': ['Yes', 'No']
        }
    },
    'readers': {
        'values': ['everyone']
    },
    'signatures': {
        'values-regex': '\\(anonymous\\)'
    },
    'writers': {
        'values-regex': '\\(anonymous\\)'
    }
}

reviewer_invitation= Invitation('ICLR.cc/2017/conference',
                                'reviewer_invitation', 
                                readers=['everyone'],
                                writers=['ICLR.cc/2017/conference'], 
                                invitees=['everyone'],
                                signatures=['ICLR.cc/2017/conference'], 
                                reply=reviewer_invitation_reply, 
                                process='../process/responseInvitationProcess_iclr2017.js', 
                                web='../webfield/web-field-invitation.html')

invitations = [submission_invitation, reference_invitation, reviewer_invitation]

## Post the invitations
for i in invitations:
    print "Posting invitation: "+i.id
    openreview.post_invitation(i)

reviewers_invited = openreview.get_group('ICLR.cc/2017/conference/reviewers-invited').members
print "reviewers invited:"+str(reviewers_invited)


## For each candidate reviewer, send an email asking them to confirm or reject the request to review
for count, reviewer in enumerate(reviewers_invited):
    print "Sending message to "+reviewer
    hashkey = openreview.get_hash(reviewer, "4813408173804203984")
    url = baseurl+"/invitation?id=" + reviewer_invitation.id+ "&email=" + reviewer + "&key=" + hashkey + "&response="
    message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
    message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
    message = message+ url + "Yes\n\n"
    message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
    message = message+ url + "No\n\n" + "Thank you"

    openreview.send_mail("OpenReview invitation response", [reviewer], message)
