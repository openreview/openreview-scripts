#!/usr/bin/python

"""
This is the initialization script for the workshop portion of ICLR 2017

It should only be run ONCE to kick off the workshop, after superuser-init.py has already been run. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
import openreview
from subprocess import call

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

groups = []

overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False
def overwrite_allowed(groupid):
    if not client.exists(groupid) or overwrite==True:
        return True
    else:
        return False

call(["node", "../../scripts/processToFile.js", "../process/submissionProcess_workshop.template", "../process"])

if client.user['id'].lower()=='openreview.net':

    # We're going to populate the list of workshop/reviewers from the list of conference/reviewers-invited,
    # so we only need to create groups for the reviewers themselves ('ICLR.cc/2017/workshop/reviewers') and
    # for the list of reviewers that have been emailed about serving as a workshop reviewer.

    if overwrite_allowed('ICLR.cc/2017/workshop'):
        iclr2017workshop = openreview.Group('ICLR.cc/2017/workshop',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017','ICLR.cc/2017/pcs','ICLR.cc/2017/workshop'],
            signatures  = ['ICLR.cc/2017'],
            signatories = ['ICLR.cc/2017/workshop'],
            members     = ['ICLR.cc/2017/pcs'],
            web         = '../webfield/iclr2017workshop_webfield.html')
        groups.append(iclr2017workshop)

    if overwrite_allowed('ICLR.cc/2017/workshop/reviewers-emailed'):
        iclr2017reviewersemailed = openreview.Group('ICLR.cc/2017/workshop/reviewers-emailed',
            readers=['ICLR.cc/2017/pcs','ICLR.cc/2017'],
            writers=['ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017/pcs'],
            signatories=['ICLR.cc/2017/workshop/reviewers-emailed'],
            members=[])
        groups.append(iclr2017reviewersemailed)

    if overwrite_allowed('ICLR.cc/2017/workshop/reviewers'):
        iclr2017reviewers = openreview.Group('ICLR.cc/2017/workshop/reviewers',
            readers=['everyone'],
            writers=['ICLR.cc/2017/workshop','ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017/workshop'],
            signatories=['ICLR.cc/2017/workshop/reviewers'],
            members=['ICLR.cc/2017/pcs'])
        groups.append(iclr2017reviewers)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        client.post_group(g)



    ## Create the submission invitation
    reply = {
        'forum': None,
        'replyto': None,
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
                'value-regex': '.{1,250}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 3,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 4,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv (link must begin with http(s) and end with .pdf)',
                'order': 5,
                'value-regex': 'upload|(http|https):\/\/.+\.pdf',
                'required':True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-dropdown': [
                    'Theory',
                    'Computer vision',
                    'Speech',
                    'Natural language processing',
                    'Deep learning',
                    'Unsupervised Learning',
                    'Supervised Learning',
                    'Semi-Supervised Learning',
                    'Reinforcement Learning',
                    'Transfer Learning',
                    'Multi-modal learning',
                    'Applications',
                    'Optimization',
                    'Structured prediction',
                    'Games'
                ]

            },
            'conflicts': {
                'description': 'Comma separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
                'order': 100,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            }
        }
    }

    submission_reply=reply.copy()

    submission_invitation = openreview.Invitation( 'ICLR.cc/2017/workshop',
        'submission',
        readers=['everyone'],
        writers=['ICLR.cc/2017/workshop'],
        invitees=['~'],
        signatures=['ICLR.cc/2017/pcs'],
        reply=submission_reply,
        duedate=1478380500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        process='../process/submissionProcess_workshop.js')

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
            'values': ['OpenReview.net']
        },
        'signatures': {
            'values-regex': '\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '\\(anonymous\\)'
        }
    }

    reviewer_invitation = openreview.Invitation('ICLR.cc/2017/workshop',
        'reviewer_invitation',
        readers=['everyone'],
        writers=['ICLR.cc/2017/workshop'],
        invitees=['everyone'],
        signatures=['ICLR.cc/2017/workshop'],
        reply=reviewer_invitation_reply,
        process='../process/responseInvitationProcess_workshop.js',
        web='../webfield/web-field-invitation.html')

    invitations = [submission_invitation, reviewer_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        client.post_invitation(i)

