#!/usr/bin/python

"""
This is the initialization script for a legacy conference.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *
from subprocess import call

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

CONFERENCE = 'AKBC.ws/2013'
# COCHAIRS = CONFERENCE + "/Program_Co-Chairs"
# SPC = CONFERENCE + "/Senior_Program_Committee"
# PC = CONFERENCE + "/Program_Committee"


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

    if overwrite_allowed(CONFERENCE):
        akbc2013 = Group(CONFERENCE,
            readers     = ['everyone'],
            writers     = [CONFERENCE],
            signatures  = ['OpenReview.net'],
            signatories = [CONFERENCE],
            members     = [],
            web         = '../webfield/akbc2013_webfield.html')
        groups.append(akbc2013)

    #
    # if overwrite_allowed(COCHAIRS):
    #     Program_Chairs = Group(COCHAIRS,
    #         readers     = [CONFERENCE, COCHAIRS, SPC, PC],
    #         writers     = [CONFERENCE],
    #         signatures  = [CONFERENCE],
    #         signatories = [COCHAIRS],
    #         members     = [])
    #     groups.append(Program_Chairs)
    #
    #
    # if overwrite_allowed(SPC):
    #     spc = Group(SPC,
    #         readers     = [CONFERENCE, COCHAIRS, SPC, PC],
    #         writers     = [CONFERENCE], #the conference needs to be a writer whenever the process functions need to modify the group
    #         signatures  = [CONFERENCE],
    #         signatories = [SPC],
    #         members     = [])
    #     groups.append(spc)
    #
    # if overwrite_allowed(PC):
    #     pc = Group(PC,
    #         readers     = [CONFERENCE, COCHAIRS, SPC, PC],
    #         writers     = [CONFERENCE],
    #         signatures  = [CONFERENCE],
    #         signatories = [PC],
    #         members     = [])
    #     groups.append(pc)

    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)

    openreview.post_group(openreview.get_group('host'),CONFERENCE)
    openreview.add_members_to_group(openreview.get_group('host'),CONFERENCE)



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
                'values-dropdown': [          ]

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

    submission_invitation = Invitation(CONFERENCE,
        'submission',
        readers=['everyone'],
        writers= ['OpenReview.net'],
        invitees=['~'],
        signatures= ['OpenReview.net'],
        reply=submission_reply,
        duedate=1369422751717)

    invitations = [submission_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)


else:
    print "Aborted. User must be Super User."
