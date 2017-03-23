#!/usr/bin/python

"""
This is the initialization script for CVPR 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import openreview
from cvprdata import *
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

if client.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################

    if not client.exists('cv-foundation.org'):
        cvfoundation = openreview.Group('cv-foundation.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(cvfoundation)

    if not client.exists('cv-foundation.org/CVPR'):
        cvpr = openreview.Group('cv-foundation.org/CVPR',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(cvpr)

    if not client.exists('cv-foundation.org/CVPR/2017'):
        cvpr2017 = openreview.Group('cv-foundation.org/CVPR/2017',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(cvpr2017)

    if overwrite_allowed(CONFERENCE):
        conf = openreview.Group(CONFERENCE,
            readers     = ['everyone'],
            writers     = [CONFERENCE],
            signatures  = ['OpenReview.net'],
            signatories = [CONFERENCE],
            members     = [ADMIN],
            web         = '../webfield/cvpr2017_webfield.html')
        groups.append(conf)

    if overwrite_allowed(COCHAIRS):
        Program_Chairs = openreview.Group(COCHAIRS,
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [COCHAIRS],
            members     = [])
        groups.append(Program_Chairs)

    if overwrite_allowed(REVIEWERS):
        reviewers = openreview.Group(REVIEWERS,
            readers     = [CONFERENCE, COCHAIRS, REVIEWERS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [REVIEWERS],
            members     = []) #more to be added later, from the list of Program_Committee members
        groups.append(reviewers)

    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        client.post_group(g)

    client.post_group(client.get_group('host').add_member(CONFERENCE))


    #########################
    ##  SETUP INVITATIONS  ##
    #########################
    call(["node", "../../scripts/processToFile.js", "../process/submissionProcess.template", "../process"])

    invitations = []

    ## Create the submission invitation, form, and add it to the list of invitations to post
    submission_invitation = openreview.Invitation(CONFERENCE+'/-/Submission',
        readers = ['everyone'],
        writers = [CONFERENCE],
        invitees = ['~'],
        signatures = [CONFERENCE],
        duedate = EIGHT_PG_TIMESTAMP_DUE,
        process = '../process/submissionProcess.js')

    submission_invitation.reply = {
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
                'description': 'Comma separated list of author names.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above. Be sure each email address is linked to the each author profile.',
                'order': 3,
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'paper length': {
                'description': 'Type of paper.',
                'order': 0,
                'value-radio':  [
                    '8 page',
                    '4 page'
                ],
                'required': True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 7,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 8,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf)',
                'order': 9,
                'value-regex': 'upload',
                'required':True
            },
            'conflicts': {
                'description': 'Comma separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
                'order': 9,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required': True
            }
        }
    }

    invitations.append(submission_invitation)

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        client.post_invitation(i)

else:
    print "Aborted. User must be Super User."
