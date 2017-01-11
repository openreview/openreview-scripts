#!/usr/bin/python

"""
This is the initialization script for ICLR 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = []
overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False
def overwrite_allowed(groupid):
    if not openreview.exists(groupid) or overwrite==True:
        return True
    else:
        return False

if openreview.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################

    if overwrite_allowed('ICLR.cc'):
        iclr            = Group('ICLR.cc',
            readers     = ['OpenReview.net'],
            writers     = ['OpenReview.net','ICLR.cc/2017/pcs'],
            signatures  = ['OpenReview.net'],
            signatories = ['ICLR.cc','ICLR.cc/2017/pcs'],
            members     = [] )
        groups.append(iclr)


    if overwrite_allowed('ICLR.cc/2017'):
        iclr2017        = Group('ICLR.cc/2017',
            readers     = ['everyone'],
            writers     = ['ICLR.cc','ICLR.cc/2017','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc'],
            signatories = ['ICLR.cc/2017','ICLR.cc/2017/pcs'],
            members     = ['ICLR.cc/2017/pcs'],
            web         = '../webfield/iclr2017_webfield.html')
        groups.append(iclr2017)


    if overwrite_allowed('ICLR.cc/2017/conference'):
        iclr2017conference = Group('ICLR.cc/2017/conference',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017','ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
            members     = ['ICLR.cc/2017/pcs'],
            web         = '../webfield/iclr2017conference_webfield.html')
        groups.append(iclr2017conference)


    if overwrite_allowed('ICLR.cc/2017/conference/organizers'):
        iclr2017conferenceorganizers = Group('ICLR.cc/2017/conference/organizers',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/organizers','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017/conference'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs', 'ICLR.cc/2017/conference/organizers'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/conference'])
        groups.append(iclr2017conferenceorganizers)


    if overwrite_allowed('ICLR.cc/2017/conference/ACs_and_organizers'):
        iclr2017conferenceACsOrganizers = Group('ICLR.cc/2017/conference/ACs_and_organizers',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/ACs_and_organizers','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017/conference'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/ACs_and_organizers'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference'])
        groups.append(iclr2017conferenceACsOrganizers)


    if overwrite_allowed('ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers'):
        iclr2017reviewersACsOrganizers = Group('ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017/conference'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference/reviewers','ICLR.cc/2017/conference'])
        groups.append(iclr2017reviewersACsOrganizers)


    if overwrite_allowed('ICLR.cc/2017/workshop'):
        iclr2017workshop = Group('ICLR.cc/2017/workshop',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017','ICLR.cc/2017/pcs','ICLR.cc/2017/workshop'],
            signatures  = ['ICLR.cc/2017'],
            signatories = ['ICLR.cc/2017/workshop'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'],
            web         = '../webfield/iclr2017workshop_webfield.html')
        groups.append(iclr2017workshop)


    if overwrite_allowed('ICLR.cc/2017/pcs'):
        iclr2017programchairs = Group('ICLR.cc/2017/pcs',
            readers=['everyone'],
            writers=['ICLR.cc/2017','ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017'],
            signatories=['ICLR.cc/2017/pcs'],
            members=[])
        groups.append(iclr2017programchairs)


    if overwrite_allowed('ICLR.cc/2017/areachairs'):
        iclr2017areachairs = Group('ICLR.cc/2017/areachairs',
            readers=['everyone'],
            writers=['ICLR.cc/2017','ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017'],
            signatories=['ICLR.cc/2017/areachairs'],
            members=[])
        groups.append(iclr2017areachairs)



    if overwrite_allowed('ICLR.cc/2017/conference/reviewers-invited'):
        iclr2017reviewersinvited = Group('ICLR.cc/2017/conference/reviewers-invited',
            readers=['ICLR.cc/2017/pcs','ICLR.cc/2017'],
            writers=['ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017/pcs'],
            signatories=['ICLR.cc/2017/conference/reviewers-invited'],
            members=[])
        groups.append(iclr2017reviewersinvited)

    if overwrite_allowed('ICLR.cc/2017/conference/reviewers-emailed'):
        iclr2017reviewersemailed = Group('ICLR.cc/2017/conference/reviewers-emailed',
            readers=['ICLR.cc/2017/pcs','ICLR.cc/2017'],
            writers=['ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017/pcs'],
            signatories=['ICLR.cc/2017/conference/reviewers-emailed'],
            members=[])
        groups.append(iclr2017reviewersemailed)


    if overwrite_allowed('ICLR.cc/2017/conference/reviewers'):
        iclr2017reviewers = Group('ICLR.cc/2017/conference/reviewers',
            readers=['everyone'],
            writers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017/conference'],
            signatories=['ICLR.cc/2017/conference/reviewers'],
            members=[])
        groups.append(iclr2017reviewers)


    if overwrite_allowed('ICLR.cc/2017/conference/reviewers-declined'):
        iclr2017reviewersdeclined = Group('ICLR.cc/2017/conference/reviewers-declined',
            readers=['everyone'],
            writers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
            signatures=['ICLR.cc/2017/conference'],
            signatories=['ICLR.cc/2017/conference/reviewers'],
            members=[])
        groups.append(iclr2017reviewersdeclined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)

    openreview.add_members_to_group(openreview.get_group('host'),'ICLR.cc/2017')




    #########################
    ##  SETUP INVITATIONS  ##
    #########################


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

    submission_invitation = Invitation( 'ICLR.cc/2017/conference',
        'submission',
        readers=['everyone'],
        writers=['ICLR.cc/2017/conference'],
        invitees=['~'],
        signatures=['ICLR.cc/2017/pcs'],
        reply=submission_reply,
        duedate=1478380500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        process='../process/submissionProcess_conference.js')

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

    reviewer_invitation = Invitation('ICLR.cc/2017/conference',
        'reviewer_invitation',
        readers=['everyone'],
        writers=['ICLR.cc/2017/conference'],
        invitees=['everyone'],
        signatures=['ICLR.cc/2017/conference'],
        reply=reviewer_invitation_reply,
        process='../process/responseInvitationProcess_iclr2017.js',
        web='../webfield/web-field-invitation.html')

    invitations = [submission_invitation, reviewer_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)



else:
    print "Aborted. User must be Super User."
