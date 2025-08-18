import argparse
import csv
import getpass
import sys
import re
import openreview
import requests
from config import *

def make_copyright_invitation(submissionId, number, authors):
    reply = {
        'forum': submissionId,
        'replyto': submissionId,
        'writers': {
            'values-regex': '~.*'
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'readers': {
            'values': [authors, COCHAIRS, CONFERENCE],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': {
            'title': {
                'order': 0,
                'value': 'Paper{0} Copyright Form'.format(number),
                'required': True
            },
            'pdf': {
                'description': 'Upload a copyright PDF form',
                'order': 1,
                'value-regex': 'upload',
                'required':True
            },
        }
    }

    invitation = openreview.Invitation(id = CONFERENCE + '/-/Paper' + str(number) + '/Copyright/Form',
        duedate = 1498867199000, #Friday, June 30, 2017 11:59:59 PM GMT
        signatures = [CONFERENCE],
        writers = [CONFERENCE],
        invitees = [authors],
        noninvitees = [],
        readers = [CONFERENCE, authors, COCHAIRS],
        reply = reply)

    return invitation

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')

for n in submissions:
    authors = 'auai.org/UAI/2017/Paper{0}/Authors'.format(n.number)
    inv = make_copyright_invitation(n.forum, n.number, authors)
    print "posting Paper{0}".format(n.number)
    client.post_invitation(inv)
