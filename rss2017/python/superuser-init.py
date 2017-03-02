#!/usr/bin/python

"""
This is the initialization script for RSS 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
import openreview
from rssdata import *
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

# Overwrite: this script is supposed to only be run once, but in reality it is usually tweaked and rerun.
# If the project isn't in use yet it is OK to overwrite the groups, however if the project is in use,
# we don't want to override the groups as people may have already been added to them.
# Overwrite false - create new groups, but doesn't overwrite existing groups
# Overwrite true - recreate from scratch
overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False
def overwrite_allowed(groupid):
    if not client.exists(groupid) or overwrite==True:
        return True
    else:
        return False

# processToFile takes a template file, turns it into a js file and inserts
# process function code in as indicated by << >>
call(["node", "../../scripts/processToFile.js", "../process/submissionProcess.template", "../process"])

if client.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################
    # These groups represents the entities and the hierarchical structure and
    # may not be actual groups of people
    if overwrite_allowed('roboticsfoundation.org'):
        a_rss = openreview.Group('roboticsfoundation.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(a_rss)


    if overwrite_allowed('roboticsfoundation.org/RSS'):
        rss = openreview.Group('roboticsfoundation.org/RSS',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(rss)

    if overwrite_allowed(CONFERENCE):
        rss2017 = openreview.Group(CONFERENCE,
            readers     = ['everyone'],
            writers     = [CONFERENCE],
            signatures  = ['OpenReview.net'],
            signatories = [CONFERENCE],
            members     = [ADMIN],
            web         = '../webfield/rss2017_webfield.html')
        groups.append(rss2017)

    # PAM change to Karthik and Shayegan when have official id's
    if overwrite_allowed(COCHAIRS):
        Program_Chairs = openreview.Group(COCHAIRS,
            readers     = [CONFERENCE, COCHAIRS, REVIEWERS],
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
    invitations = []

    ## Create the submission invitation, form, and add it to the list of invitations to post
    submission_invitation = openreview.Invitation(CONFERENCE,
        'submission',
        readers = ['everyone'],
        writers = [CONFERENCE],
        # ~ is a special group of all registered accounts
        invitees = ['~'],
        signatures = [CONFERENCE],
        duedate=TIMESTAMP_DUE,
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
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'content': {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            # [^;,\\n] means all chars except ';' ',' and '\n'
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                # PAM put as a 'constant' up top
                # 2 or more lower case letters, numbers, _'s, -'s or .'s
                # then @
                # then 2 or more letters/numbers (like before)
                # then a .
                # then 2 or more letters only
                # then shows that with a comma for zero or more times followed by at least one proper expression
                # i.e. a list of email addresses
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 4,
                # PAM is this up to 5,000 words, because \\S is not white space followed by \\s which is white space
                'value-regex': '[\\S\\s]{1,5000}',
                'required': True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*"
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 7,
                # up to 250 chars with no line return
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },

            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf)',
                'order': 8,
                'value-regex': 'upload',
                'required':True
            },
            'conflicts': {
                'description': 'Comma separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
                'order': 9,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required': True
            },
            'student paper': {
                'description': 'Is this a student paper?',
                'order': 10,
                'value-radio': [
                    'Yes',
                    'No'
                ]
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
