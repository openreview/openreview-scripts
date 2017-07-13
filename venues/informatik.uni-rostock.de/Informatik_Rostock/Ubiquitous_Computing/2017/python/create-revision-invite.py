#!/usr/bin/python

import argparse
import sys
import os
import openreview
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.SUBMISSION)

def create_revision_invitation(n):
    revision_invitation = openreview.Invitation(config.CONF + '/-/Paper{0}/Add/Revision'.format(n.number), **config.revision_params)
    revision_invitation.invitees = [config.CONF + '/Paper{0}/Authors'.format(n.number)]
    revision_invitation.reply = config.submission_reply
    revision_invitation.reply['referent'] = n.forum
    revision_invitation.reply['forum'] = n.forum
    return revision_invitation

for n in submissions:
    print n.number
    client.post_invitation(create_revision_invitation(n))
