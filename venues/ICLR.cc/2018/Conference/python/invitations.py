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
import requests
import config

maskAuthorsGroup = config.CONF + "/Paper[PAPER_NUMBER]/Authors"
maskReviewerGroup = config.CONF + "/Paper[PAPER_NUMBER]/Reviewers"
maskAreaChairGroup = config.CONF + "/Paper[PAPER_NUMBER]/Area_Chair"
maskAnonReviewerGroup = config.CONF + "/Paper[PAPER_NUMBER]/AnonReviewer[0-9]+"

invitation_configurations = {
    'Add_Revision': {
        'byPaper': True,
        'invitees': [maskAuthorsGroup]
    },
    'Public_Comment': {
        'byPaper': False,
        'invitees': ['~']
    },
    'Official_Comment': {
        'byPaper': True,
        'invitees': [maskReviewerGroup, maskAuthorsGroup, maskAreaChairGroup],
        'signatures': [maskAnonReviewerGroup, maskAuthorsGroup, maskAreaChairGroup],
        'byForum': True,
        'params': config.official_comment_params
    },
    'Official_Review': {
        'byPaper': True,
        'invitees': [maskReviewerGroup],
        'byForum': True,
        'byReplyTo': True,
        'params': config.official_review_params
    },
    'Meta_Review': {
        'byPaper': True,
        'byForum': True,
        'byReplyTo': True,
        'invitees': [maskAreaChairGroup],
        'signatures': [maskAreaChairGroup],
        'params': config.meta_review_params
    },
    'Add_Bid': {
        'tags': True,
        'byPaper': False,
        'invitees': [config.REVIEWERS]
    },
    'Recommend_Reviewer': {
        'tags': True,
        'byPaper': True,
        'invitees': [maskAreaChairGroup]
    }
}

def get_or_create_invitations(invitationId, overwrite):
    invitation_config = invitation_configurations[invitationId]
    if invitation_config['byPaper']:
        print "by paper ", invitationId
        papers = client.get_notes(invitation = config.BLIND_SUBMISSION)
        invitations = client.get_invitations(regex = config.CONF + '/-/Paper[^\/]*/' + invitationId, tags = invitation_config.get('tags'))
        print 'invitations', [i.id for i in invitations]
        if invitations and len(invitations) == len(papers) and not overwrite:
            # TODO: why is this here? why not just return invitations?
            return [i for i in invitations if re.match(config.CONF + '/-/Paper[0-9]+/' + invitationId, i.id)]
        else:
            print "Some or all of the invitations do not exist. Generating invitations."
            invitations = []
            for n in papers:
                new_invitation = openreview.Invitation(config.CONF + '/-/Paper{0}/'.format(n.number) + invitationId, **invitation_config['params'])

                if 'byForum' in invitation_config:
                    new_invitation.reply['forum'] = n.forum

                if 'byReplyTo' in invitation_config:
                    new_invitation.reply['replyto'] = n.forum

                if 'signatures' in invitation_config:
                    new_invitation.reply['signatures']['values-regex'] = prepare_regex(new_invitation.id, invitation_config['signatures'])

                print new_invitation.id
                invitations.append(client.post_invitation(new_invitation))
            return invitations
    else:
        try:
            invitation = client.get_invitation(config.CONF + '/-/' + invitationId)
            return [invitation]
        except openreview.OpenReviewException as error:
            if error[0][0]['type'].lower() == 'not found':
                print "Invitation does not exist. Generating invitation."
                new_invitation = openreview.Invitation(config.CONF + '/-/' + invitationId, **invitation_config['params'])
                print new_invitation.id
                return client.post_invitation(new_invitation)
            else:
                raise error

def prepare_invitees(invitationId, invitees):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        return [ invitee.replace('[PAPER_NUMBER]', match.group(1)) for invitee in invitees]
    else:
        return invitees

def prepare_regex(invitationId, members):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        return '|'.join([ member.replace('[PAPER_NUMBER]', match.group(1)) for member in members])
    else:
        return members

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('invitation', help="invitation id: " + ", ".join(invitation_configurations.keys()))
parser.add_argument('--enable', action='store_true', help="if present, enables the given invitation")
parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.invitation in invitation_configurations:
    if args.enable or args.disable:
        invitationId = args.invitation
        enable = args.enable and not args.disable

        client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

        invitations = get_or_create_invitations(invitationId, args.overwrite)
        updated = 0

        if invitations:
            for i in invitations:

                i.invitees = prepare_invitees(i.id, invitation_configurations[invitationId]['invitees']) if enable else []

                result = client.post_invitation(i)
                print "SUCCESS: {0}, {1}".format(result.id, i.invitees)
                updated += 1
        else:
            print "Invitation not found: ", invitationId

        print "# Invitations updated: ", updated

    else:
        print "Invalid enable value: ", args.enable

else:
    print "Invalid invitation: ", args.invitation




