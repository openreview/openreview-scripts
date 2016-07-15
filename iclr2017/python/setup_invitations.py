## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
args = parser.parse_args()

import os, sys
import csv
import pydash
import requests
import params

sys.path.append('../..')
from client import *

## Initialize the client library with username and password
or3 = Client(args.username,args.password)





## Create the submission invitation
submission_reply = {
    'forum': None,
    'parent': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'Your displayed identity associated with the above content.',
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
submission_invitation = Invitation('ICLR.cc/2017/conference','submission', readers=['everyone'], invitees=['~'], reply=submission_reply, process='../process/submissionProcess_iclr2017.js')

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
reviewer_invitation = Invitation('ICLR.cc/2017','reviewer_invitation', readers=['everyone'], invitees=['everyone'], reply=reviewer_invitation_reply, process='../process/responseInvitationProcess_iclr2017.js', web='../webfield/web-field-invitation.html')

invitations = [submission_invitation, reviewer_invitation]

## Post the invitations
for i in invitations:
    print "Posting invitation: "+i.body['id']
    or3.set_invitation(i.body)



reviewers_invited = or3.get_group({'id':'ICLR.cc/2017/reviewers-invited'}).json()['groups'][0]['members']


## For each candidate reviewer, send an email asking them to confirm or reject the request to review
for count, reviewer in enumerate(reviewers_invited):
    print "Sending message to "+reviewer
    hashkey = or3.get_hash(reviewer, reviewer_invitation.body['id'])
    url = "http://localhost:3000/invitation?id=" + reviewer_invitation.body['id'] + "&email=" + reviewer + "&key=" + hashkey + "&response="
    message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
    message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
    message = message+ url + "Yes\n\n"
    message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
    message = message+ url + "No\n\n" + "Thank you"
    or3.send_mail("OpenReview invitation response", [reviewer], message)





## Define and post a sample note
note1 = {
    'content': {
        'CMT_id':'',
        'abstract':'This is note 1',
        'author_emails':"author@gmail.com",
        'authors':'Author 1',
        'conflicts':'cs.berkeley.edu',
        'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
        'title':'Note 1',
        'keywords':['keyword']
    },
    'forum': None,
    'invitation': 'ICLR.cc/2017/conference/-/submission',
    'parent': None,
    'pdfTransfer':"url",
    'readers':["everyone"],
    'signatures':["~super_user1"],
    'writers':["~super_user1"],
}

or3.set_note(note1)