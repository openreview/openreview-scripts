#!/usr/bin/python

"""
<<<<<<< e05208d8bebfb3e22cbe0ad88cf2306b18a48e74
This is the initialization script for dblp.org
=======
This is the initialization script for DBLP.org
>>>>>>> added dblp directory and tutorial section

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
    if overwrite_allowed('DBLP.org'):
        DBLP            = Group('DBLP.org',      
            readers     = ['OpenReview.net'], 
            writers     = ['OpenReview.net','DBLP.org'], 
            signatures  = ['OpenReview.net'], 
            signatories = ['DBLP.org'], 
            members     = [] )
        groups.append(DBLP)

    if overwrite_allowed('DBLP.org/upload'):
        DBLP_upload     = Group('DBLP.org/upload',
            readers     = ['DBLP.org/upload'],
            writers     = ['DBLP.org','DBLP.org/upload'],
            signatures  = ['DBLP.org'],
            signatories = ['DBLP.org/upload'],
            members     = ['spector@cs.umass.edu','mbok@cs.umass.edu','rbhat@umass.edu','asrinivasan@cs.umass.edu'] )
        groups.append(DBLP_upload)
    
    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)






    reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': ['DBLP.org/upload']
        },
        'writers': {
            'values': ['DBLP.org/upload']
        },
        'content': {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{0,100}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 2,
                'value-regex': '[\\S\\s]{0,5000}',
                'required':False
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 3,
                'value-regex': '[^,\\n]*(,[^,\\n]+)*',
                'required':False
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 4,
                'value-regex': '[^,\\n]*(,[^,\\n]+)*',
                'required':False
            },
            'DBLP_url': {
                'description': 'DBLP.org url associated with this paper',
                'order': 3,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            }
        }
    }
    submission_invitation = Invitation( 'DBLP.org',
        'paper', 
        readers=['everyone'], 
        writers=['DBLP.org/upload'],
        invitees=['DBLP.org/upload'], 
        signatures=['DBLP.org'], 
        reply=reply,
        duedate=0, #duedate of 0 means that the invitation has not been released
        process='../process/dblp_process.js')

    invitations = [submission_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)
