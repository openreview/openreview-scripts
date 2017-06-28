#!/usr/bin/python

"""

This is the initialization script for dblp.org
added dblp directory and tutorial section

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
parser.add_argument('--overwrite',
                    help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username != None and args.password != None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = []
overwrite = True if (
    args.overwrite != None and args.overwrite.lower() == 'true') else False


def overwrite_allowed(groupid):
    if not openreview.exists(groupid) or overwrite == True:
        return True
    else:
        return False


if openreview.user['id'].lower() == 'openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################
    if overwrite_allowed('DBLP.org'):
        DBLP = Group('DBLP.org',
                     readers=['OpenReview.net'],
                     writers=['OpenReview.net', 'DBLP.org'],
                     signatures=['OpenReview.net'],
                     signatories=['DBLP.org'],
                     members=[])
        groups.append(DBLP)

    if overwrite_allowed('DBLP.org/upload'):
        DBLP_upload = Group('DBLP.org/upload',
                            readers=['DBLP.org/upload'],
                            writers=['DBLP.org', 'DBLP.org/upload'],
                            signatures=['DBLP.org'],
                            signatories=['DBLP.org/upload'],
                            members=['spector@cs.umass.edu',
                                     'mbok@cs.umass.edu', 'rbhat@cs.umass.edu',
                                     'ngovindraja@cs.umass.edu', 'rbhat@umass.edu',
                                     'asrinivasan@cs.umass.edu'])
        groups.append(DBLP_upload)

    ## Post the groups
    for g in groups:
        print "Posting group: ", g.id
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
                'value-regex': '.{0,500}',
                'required': False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 2,
                'value-regex': '[\\S\\s]{0,5000}',
                'required': False
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':False
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':False
            },
            'DBLP_url': {
                'description': 'DBLP.org url associated with this paper',
                'order': 3,
                'value-regex': '[^\\n]{0,250}',
                'required': False
            },
            'isbn': {
                'description': 'isbn number of this paper',
                'order': 5,
                'value-regex': '[^\\n]{0,20}',
                'required': False

            },
            'ee': {
                'description': 'electronic edition of the paper',
                'order': 6,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'series': {
                'description': 'The name of the series the volume is a part of',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'mag_number': {
                'description': 'The number of a journal, magazine, technical '
                               'report, or of a work in a series',
                'order': 5,
                'value-regex': '[^\\n]{0,20}',
                'required': False

            },
            'month': {
                'description': 'the month in which the paper or work was published.',
                'order': 5,
                'value-regex': '[a-zA-Z]{0,20}',
                'required': False

            },
            'year': {
                'description': 'year in which paper/journal was Published',
                'order': 5,
                'value-regex': '[^\\n]{0,20}',
                'required': False

            },
            'booktitle': {
                'description': 'Title of a book, part of which is being cited',
                'order': 5,
                'value-regex': '.{0,100}',
                'required': False

            },
            'editors': {
                'description': 'Comma separated list of editor names',
                'order': 7,
                'value-regex': '[^,\\n]*(,[^,\\n]+)*',
                'required': False
            },
            'sub_type': {
                'description': 'subtype of a technical report',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'type': {
                'description': 'The type of a technical report',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'journal': {
                'description': 'A journal name.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'volume': {
                'description': 'The volume of a journal or multivolume book.',
                'order': 5,
                'value-regex': '[^\\n]{0,100}',
                'required': False

            },
            'pages': {
                'description': 'One or more page numbers or range of numbers',
                'order': 5,
                'value-regex': '[^\\n]{0,100}',
                'required': False

            },
            'crossref': {
                'description': 'The database key of the entry being cross referenced.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'chapter': {
                'description': 'A chapter (or section or whatever) number',
                'order': 5,
                'value-regex': '[^\\n]{0,8}',
                'required': False

            },
            'publisher': {
                'description': 'The publisher\'s name.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'school': {
                'description': 'The name of the school where a thesis was written.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'pub_key': {
                'description': 'a key that uniquely identifies this record. formatted as follows: <first author lastname>|<parsed title>, where <parsed title> is the title, lowercased and with spaces replaced with _ (underscore)',
                'order': 5,
                'value-regex': '[^ ]+\|[^ ]+.',
                'required': False
            }

        }
    }
    submission_invitation = Invitation('DBLP.org/-/upload',
                                       readers=['everyone'],
                                       writers=['DBLP.org/upload'],
                                       invitees=['DBLP.org/upload'],
                                       signatures=['DBLP.org'],
                                       reply=reply)


    invitations = [submission_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: " + i.id
        openreview.post_invitation(i)
