#!/usr/bin/python

"""
A script for managing invitations.

You can create, enable, or disable most invitations in ICLR 2018 from this script.

Usage:

python toggle-invitations.py Public_Comment --enable
python toggle-invitations.py Public_Comment --disable
"""

# Import statements
import argparse
import csv
import getpass
import sys
import re
import openreview
from openreview import invitations
import requests
import config
import pprint
import os

conference = 'MIDL.amsterdam/2018/Conference'
mask_authors_group = conference + "/Paper<number>/Authors"
mask_reviewers_group = conference + "/Paper<number>/Reviewers"
mask_areachair_group = conference + "/Paper<number>/Area_Chairs"
mask_anonreviewer_group = conference + "/Paper<number>/AnonReviewer[0-9]+"
mask_allusers_group = conference + "/Paper<number>/All_Users"
mask_unsubmitted_group = conference + "/Paper<number>/Reviewers/Unsubmitted"
mask_submitted_group = conference + "/Paper<number>/Reviewers/Submitted"
program_chairs_id = conference + '/Program_Chairs'
blind_submission_inv_id = conference + '/-/Blind_Submission'

invitation_templates = {
    'Add_Revision': {
        'id': conference + '/-/Paper<number>/Add/Revision',
        'readers': ['everyone'],
        'writers': [conference],
        'invitees': [mask_authors_group, program_chairs_id],
        'noninvitees': [],
        'signatures': [conference],
        'reply': dict(config.submission_reply, **{'referent': '<forum>', 'forum': '<forum>'})
    }
}

def get_invitation_template(template_id, disable=False):
    invitation_template = invitation_templates[template_id]
    if disable:
        invitation_template['invitees'] = []
    return invitation_template

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('invitations', nargs='*', help="invitation id: " + ", ".join(invitation_templates.keys()))
parser.add_argument('--numbers', nargs='+', default=[], help='paper numbers to modify')
parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation. otherwise, enables the invitation')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.invitations == ['all']:
    invitations_to_process = invitation_templates.keys()
else:
    invitations_to_process = args.invitations

assert all(id in invitation_templates.keys() for id in args.invitations), "Invalid invitation. You must choose from the following: {}".format(invitation_templates.keys())

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

papers = client.get_notes(invitation = conference + '/-/Submission')

if args.numbers:
    papers = filter(lambda x: str(x.number) in args.numbers, papers)

for paper in papers:
    for template_id in invitations_to_process:
        invitation_template = get_invitation_template(template_id, disable=args.disable)
        new_inv = invitations.from_template(invitation_template, paper)
        client.post_invitation(new_inv)

