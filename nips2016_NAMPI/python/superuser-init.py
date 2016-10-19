#!/usr/bin/python

"""
This is the initialization script for NIPS 2016 NAMPI.

It should only be run ONCE to kick off the workshop. It can only be run by the Super User.

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
    g = openreview.get_group(groupid)
    if openreview.exists(g) or overwrite==True:
        return True
    else:
        return False

print "overwrite allowed?",overwrite_allowed('NIPS.cc/2016/workshop')

if openreview.user['id'].lower()=='openreview.net':
    
    #########################
    ##    SETUP GROUPS     ##
    ######################### 

    if overwrite_allowed('NIPS.cc/2016/workshop'):
        print 'workshop made'
        nips2016_workshop = Group('NIPS.cc/2016/workshop',
            signatories = ['NIPS.cc/2016/workshop'],
            writers     = ['NIPS.cc/2016','NIPS.cc/2016/workshop'],
            members     = [],
            readers     = ['everyone'],
            signatures  = ['NIPS.cc/2016'])
        groups.append(nips2016_workshop)
    
    if overwrite_allowed('NIPS.cc/2016/workshop/NAMPI'):
        nips2016_workshop_NAMPI = Group('NIPS.cc/2016/workshop/NAMPI', 
            signatories = ['NIPS.cc/2016/workshop/NAMPI'], 
            writers     = ['NIPS.cc/2016/workshop','NIPS.cc/2016/workshop/NAMPI','NIPS.cc/2016/workshop/NAMPI/pcs'],
            members     = ['NIPS.cc/2016/workshop/NAMPI/pcs'],
            readers     = ['everyone'], 
            web         = '../webfield/NAMPI-webfield.html',
            signatures  = ['NIPS.cc/2016/workshop'])
        groups.append(nips2016_workshop_NAMPI)
        ## Add the NAMPI group to the host page
        ## NOTE: Should this be refactored into a "save to homepage" function or something like that?
        openreview.post_group(openreview.get_group('host').add_member(nips2016_workshop_NAMPI))


    if overwrite_allowed('NIPS.cc/2016/workshop/NAMPI/pcs'):
        NAMPIprogramchairs = Group('NIPS.cc/2016/workshop/NAMPI/pcs', 
            readers=['everyone'], 
            writers=['NIPS.cc/2016/workshop/NAMPI','NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatures=['NIPS.cc/2016/workshop/NAMPI'],
            signatories=['NIPS.cc/2016/workshop/NAMPI/pcs'],
            members=[])
        groups.append(NAMPIprogramchairs)


    if overwrite_allowed('NIPS.cc/2016/workshop/NAMPI/reviewers-invited'):
        NAMPIreviewersinvited = Group('NIPS.cc/2016/workshop/NAMPI/reviewers-invited', 
            readers=['NIPS.cc/2016/workshop/NAMPI/pcs','NIPS.cc/2016/workshop/NAMPI','OpenReview.net'], 
            writers=['NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatures=['NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatories=['NIPS.cc/2016/workshop/NAMPI/reviewers-invited'],
            members=[])
        groups.append(NAMPIreviewersinvited)

    if overwrite_allowed('NIPS.cc/2016/workshop/NAMPI/reviewers-emailed'):
        NAMPIreviewersemailed = Group('NIPS.cc/2016/workshop/NAMPI/reviewers-emailed', 
            readers=['NIPS.cc/2016/workshop/NAMPI/pcs','NIPS.cc/2016/workshop/NAMPI'], 
            writers=['NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatures=['NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatories=['NIPS.cc/2016/workshop/NAMPI/reviewers-emailed'],
            members=[])
        groups.append(NAMPIreviewersemailed)


    if overwrite_allowed('NIPS.cc/2016/workshop/NAMPI/reviewers'):
        NAMPIreviewers = Group('NIPS.cc/2016/workshop/NAMPI/reviewers', 
            readers=['everyone'],
            writers=['NIPS.cc/2016/workshop/NAMPI','NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatures=['NIPS.cc/2016/workshop/NAMPI'],
            signatories=['NIPS.cc/2016/workshop/NAMPI/reviewers'],
            members=[])
        groups.append(NAMPIreviewers)


    if overwrite_allowed('NIPS.cc/2016/workshop/NAMPI/reviewers-declined'):
        NAMPIreviewersdeclined = Group('NIPS.cc/2016/workshop/NAMPI/reviewers-declined',
            readers=['everyone'],
            writers=['NIPS.cc/2016/workshop/NAMPI','NIPS.cc/2016/workshop/NAMPI/pcs'],
            signatures=['NIPS.cc/2016/workshop/NAMPI'],
            signatories=['NIPS.cc/2016/workshop/NAMPI/reviewers'],
            members=[])
        groups.append(NAMPIreviewersdeclined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)







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
                'value-regex': '.{1,100}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'value-regex': '[^,\\n]+(,[^,\\n]+)*',
                'required':True
            },
            'author_emails': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                'value-regex': '[^,\\n]+(,[^,\\n]+)*',
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
                'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
                'order': 100,
                'value-regex': '([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)(\;[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)*',
                'required':True
            }
        }
    }

    submission_reply=reply.copy()
    submission_reply['referenti']=['NIPS.cc/2016/workshop/NAMPI/-/reference']

    submission_invitation = Invitation( 'NIPS.cc/2016/workshop/NAMPI',
        'submission', 
        readers=['everyone'], 
        writers=['NIPS.cc/2016/workshop/NAMPI'],
        invitees=['~'], 
        signatures=['NIPS.cc/2016/workshop/NAMPI/pcs'], 
        reply=submission_reply,
        duedate=1477055785000, #duedate of 0 means that the invitation has not been released
        process='../process/submissionProcess_NAMPI.js')

    reference_reply=reply.copy()

    reference_invitation = Invitation('NIPS.cc/2016/workshop/NAMPI',
        'reference',
        readers=['everyone'], 
        writers=['NIPS.cc/2016/workshop/NAMPI'],
        invitees=['~'], 
        signatures=['NIPS.cc/2016/workshop/NAMPI/pcs'], 
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
            'values': ['OpenReview.net']
        },
        'signatures': {
            'values-regex': '\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '\\(anonymous\\)'
        }
    }

    reviewer_invitation = Invitation('NIPS.cc/2016/workshop/NAMPI',
        'reviewer_invitation', 
        readers=['everyone'],
        writers=['NIPS.cc/2016/workshop/NAMPI'], 
        invitees=['everyone'],
        signatures=['NIPS.cc/2016/workshop/NAMPI'], 
        reply=reviewer_invitation_reply, 
        process='../process/responseInvitationProcess.js', 
        web='../webfield/NAMPI-invitation-webfield.html')

    invitations = [submission_invitation, reference_invitation, reviewer_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)



else:
    print "Aborted. User must be Super User."
