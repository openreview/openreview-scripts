#!/usr/bin/python

"""
This is the initialization script for UAI 2017.

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

    if overwrite_allowed('UAI.org'):
        uai            = Group('UAI.org',
            readers     = ['OpenReview.net'], 
            writers     = ['OpenReview.net','UAI.org/2017/pcs'],
            signatures  = ['OpenReview.net'], 
            signatories = ['UAI.org','UAI.org/2017/pcs'],
            members     = [] )
        groups.append(uai)


    if overwrite_allowed('UAI.org/2017'):
        uai2017        = Group('UAI.org/2017',
            readers     = ['everyone'],       
            writers     = ['UAI.org','UAI.org/2017','UAI.org/2017/pcs'],
            signatures  = ['UAI.org'],
            signatories = ['UAI.org/2017','UAI.org/2017/pcs'],
            members     = ['UAI.org/2017/pcs'],
            web         = '../webfield/uai2017_webfield.html')
        groups.append(uai2017)


    if overwrite_allowed('UAI.org/2017/conference'):
        uai2017conference = Group('UAI.org/2017/conference',
            readers     = ['everyone'], 
            writers     = ['UAI.org/2017','UAI.org/2017/conference','UAI.org/2017/pcs'],
            signatures  = ['UAI.org/2017'],
            signatories = ['UAI.org/2017/conference','UAI.org/2017/pcs'],
            members     = ['UAI.org/2017/pcs'],
            web         = '../webfield/uai2017conference_webfield.html')
        groups.append(uai2017conference)


    if overwrite_allowed('UAI.org/2017/conference/organizers'):
        uai2017conferenceorganizers = Group('UAI.org/2017/conference/organizers',
            readers     = ['everyone'], 
            writers     = ['UAI.org/2017/conference','UAI.org/2017/conference/organizers','UAI.org/2017/pcs'],
            signatures  = ['UAI.org/2017/conference'],
            signatories = ['UAI.org/2017/conference','UAI.org/2017/pcs', 'UAI.org/2017/conference/organizers'],
            members     = ['UAI.org/2017/pcs','UAI.org/2017/conference'])
        groups.append(uai2017conferenceorganizers)


    if overwrite_allowed('UAI.org/2017/conference/ACs_and_organizers'):
        uai2017conferenceACsOrganizers = Group('UAI.org/2017/conference/ACs_and_organizers',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference','UAI.org/2017/conference/ACs_and_organizers','UAI.org/2017/pcs'],
            signatures  = ['UAI.org/2017/conference'],
            signatories = ['UAI.org/2017/conference','UAI.org/2017/pcs','UAI.org/2017/conference/ACs_and_organizers'],
            members     = ['UAI.org/2017/pcs','UAI.org/2017/areachairs','UAI.org/2017/conference'])
        groups.append(uai2017conferenceACsOrganizers)


    if overwrite_allowed('UAI.org/2017/conference/reviewers_and_ACS_and_organizers'):
        uai2017reviewersACsOrganizers = Group('UAI.org/2017/conference/reviewers_and_ACS_and_organizers',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference','UAI.org/2017/conference/reviewers_and_ACS_and_organizers','UAI.org/2017/pcs'],
            signatures  = ['UAI.org/2017/conference'],
            signatories = ['UAI.org/2017/conference','UAI.org/2017/pcs','UAI.org/2017/conference/reviewers_and_ACS_and_organizers'],
            members     = ['UAI.org/2017/pcs','UAI.org/2017/areachairs','UAI.org/2017/conference/reviewers','UAI.org/2017/conference'])
        groups.append(uai2017reviewersACsOrganizers)


    #


    if overwrite_allowed('UAI.org/2017/pcs'):
        uai2017programchairs = Group('UAI.org/2017/pcs',
            readers=['everyone'], 
            writers=['UAI.org/2017','UAI.org/2017/pcs'],
            signatures=['UAI.org/2017'],
            signatories=['UAI.org/2017/pcs'],
            members=[])
        groups.append(uai2017programchairs)


    if overwrite_allowed('UAI.org/2017/areachairs'):
        uai2017areachairs = Group('UAI.org/2017/areachairs',
            readers=['everyone'],
            writers=['UAI.org/2017','UAI.org/2017/pcs'],
            signatures=['UAI.org/2017'],
            signatories=['UAI.org/2017/areachairs'],
            members=[])
        groups.append(uai2017areachairs)



    if overwrite_allowed('UAI.org/2017/conference/reviewers-invited'):
        uai2017reviewersinvited = Group('UAI.org/2017/conference/reviewers-invited',
            readers=['UAI.org/2017/pcs','UAI.org/2017'],
            writers=['UAI.org/2017/pcs'],
            signatures=['UAI.org/2017/pcs'],
            signatories=['UAI.org/2017/conference/reviewers-invited'],
            members=[])
        groups.append(uai2017reviewersinvited)

    if overwrite_allowed('UAI.org/2017/conference/reviewers-emailed'):
        uai2017reviewersemailed = Group('UAI.org/2017/conference/reviewers-emailed',
            readers=['UAI.org/2017/pcs','UAI.org/2017'],
            writers=['UAI.org/2017/pcs'],
            signatures=['UAI.org/2017/pcs'],
            signatories=['UAI.org/2017/conference/reviewers-emailed'],
            members=[])
        groups.append(uai2017reviewersemailed)


    if overwrite_allowed('UAI.org/2017/conference/reviewers'):
        uai2017reviewers = Group('UAI.org/2017/conference/reviewers',
            readers=['everyone'],
            writers=['UAI.org/2017/conference/reviewers','UAI.org/2017/pcs'],
            signatures=['UAI.org/2017/conference'],
            signatories=['UAI.org/2017/conference/reviewers'],
            members=[])
        groups.append(uai2017reviewers)


    if overwrite_allowed('UAI.org/2017/conference/reviewers-declined'):
        uai2017reviewersdeclined = Group('UAI.org/2017/conference/reviewers-declined',
            readers=['everyone'],
            writers=['UAI.org/2017/conference','UAI.org/2017/pcs'],
            signatures=['UAI.org/2017/conference'],
            signatories=['UAI.org/2017/Reviewers'],
            members=[])
        groups.append(uai2017reviewersdeclined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)
    openreview.post_group(openreview.get_group('host').add_member('UAI.org/2017'))

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

    submission_invitation = Invitation( 'UAI.org/2017/conference',
        'submission', 
        readers=['everyone'], 
        writers=['UAI.org/2017/conference'],
        invitees=['~'], 
        signatures=['UAI.org/2017/pcs'],
        reply=submission_reply,
        duedate=1578380500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        process='../process/submissionProcess_uai2017.js')

    ## Create 'request for availability to review' invitation
    reviewer_invitation_reply = {
        'forum': {
            'value-regex': 'UAI.org/2017/conference/reviewers/~.*'
        },
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

    reviewer_invitation = Invitation('UAI.org/2017/conference',
        'reviewer_invitation',
        readers=['everyone'],
        writers=['UAI.org/2017/conference'],
        invitees=['everyone'],
        signatures=['UAI.org/2017/conference'],
        reply=reviewer_invitation_reply, 
            process='../process/responseInvitationProcess_uai2017.js',
        web='../webfield/web-field-invitation.html')

    paper_invitation_reply = {
        'content': {}
    }

    paper_meta_invitation = Invitation('UAI.org/2017/conference',
                                       'matching',
                                       signatures=['UAI.org/2017/pcs'],
                                       readers=['everyone'],
                                       writers=['everyone'], reply=paper_invitation_reply)

    invitations = [submission_invitation,reviewer_invitation,paper_meta_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)



else:
    print "Aborted. User must be Super User."
