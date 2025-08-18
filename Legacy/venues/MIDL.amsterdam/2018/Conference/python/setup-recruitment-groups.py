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

group_templates = {
    'Reviewers/Invited': {
        'id': 'MIDL.amsterdam/2018/Conference/Paper<number>/Reviewers/Invited',
        'readers': [conference],
        'writers': [conference],
        'signatures': [conference],
        'signatories': [],
        'members': []
    },
    'Reviewers/Declined': {
        'id': 'MIDL.amsterdam/2018/Conference/Paper<number>/Reviewers/Declined',
        'readers': [conference],
        'writers': [conference],
        'signatures': [conference],
        'signatories': [],
        'members': []
    },
    'Reviewers/Accepted': {
        'id': 'MIDL.amsterdam/2018/Conference/Paper<number>/Reviewers/Accepted',
        'readers': [conference],
        'writers': [conference],
        'signatures': [conference],
        'signatories': [],
        'members': []
    }

}

def get_group_template(template_id, disable=False):
    invitation_template = group_templates[template_id]
    if disable:
        invitation_template['invitees'] = []
    return invitation_template

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('groups', nargs='*', help="invitation id: " + ", ".join(group_templates.keys()))
parser.add_argument('--numbers', nargs='+', default=[], help='paper numbers to modify')
parser.add_argument('--overwrite', action='store_true', help='if present, overwrites the groups')
parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation. otherwise, enables the invitation')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.groups == ['all']:
    groups_to_process = group_templates.keys()
else:
    groups_to_process = args.groups

assert all(id in group_templates.keys() for id in groups_to_process), "Invalid group. You must choose from the following: {}".format(group_templates.keys())

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

papers = client.get_notes(invitation = conference + '/-/Submission')

if args.numbers:
    papers = filter(lambda x: str(x.number) in args.numbers, papers)

for paper in papers:
    for template_id in groups_to_process:
        group_template = get_group_template(template_id, disable=args.disable)
        new_group = openreview.Group(**invitations.fill_template(group_template, paper))
        if (not client.exists(new_group.id)) or args.overwrite:
            client.post_group(new_group)
        else:
            print "exists; skipping ", new_group.id

